import logging
import os
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
import chromadb

from config import GEMINI_API_KEY, VECTORSTORE_CONFIG, MODEL_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def load_and_split_documents(self, directory_path: str) -> List[Any]:
        """Load and split documents from a directory"""
        documents = []
        directory_path = os.path.abspath(directory_path)
        
        if not os.path.exists(directory_path):
            logger.error(f"Directory does not exist: {directory_path}")
            return []
        
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                try:
                    if not os.path.exists(file_path):
                        logger.error(f"File does not exist: {file_path}")
                        continue
                    
                    # Read the file content directly
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        if not text.strip():
                            logger.error(f"File is empty: {file_path}")
                            continue
                        
                        # Create document with metadata
                        doc = Document(
                            page_content=text,
                            metadata={
                                "source": filename,
                                "file_path": file_path
                            }
                        )
                        documents.append(doc)
                        logger.info(f"Successfully loaded document from {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {str(e)}")
                    continue
        
        if not documents:
            logger.error(f"No documents were loaded from {directory_path}")
            return []
        
        try:
            # Split documents into chunks
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Successfully split {len(documents)} documents into {len(split_docs)} chunks")
            return split_docs
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            return []

class VectorStoreManager:
    def __init__(self, google_api_key: str, persist_directory: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )
        self.persist_directory = persist_directory
        self.client_settings = chromadb.config.Settings(
            anonymized_telemetry=False,
            persist_directory=persist_directory,
            is_persistent=True
        )
    
    def create_chroma_db(self, documents: List[Any]) -> None:
        """Create a Chroma vector store from documents"""
        try:
            Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                client_settings=self.client_settings
            )
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def load_chroma_db(self) -> Chroma:
        """Load an existing Chroma vector store"""
        try:
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                client_settings=self.client_settings
            )
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise

def process_document_directory(input_dir: str, output_dir: str) -> List[Dict[str, Any]]:
    """Process PDF and DOCX documents in a directory"""
    metadata_list = []
    
    # Convert to absolute paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    
    # Verify input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Input directory does not exist: {input_dir}")
        return []
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{Path(filename).stem}.txt")
            
            if not os.path.exists(input_path):
                logger.error(f"PDF file does not exist: {input_path}")
                continue
                
            try:
                # Open PDF document
                doc = fitz.open(input_path)
                
                if doc.page_count == 0:
                    logger.error(f"PDF file is empty: {filename}")
                    continue
                
                # Extract text from each page
                text = ""
                for page in doc:
                    text += page.get_text()
                
                if not text.strip():
                    logger.error(f"No text content extracted from {filename}")
                    continue
                
                # Save extracted text
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Add metadata
                metadata_list.append({
                    'source': filename,
                    'type': 'pdf',
                    'path': output_path
                })
                
                logger.info(f"Processed {filename}")
                
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                continue
            
            finally:
                if 'doc' in locals():
                    doc.close()
    
    if not metadata_list:
        logger.error(f"No PDF documents were processed in {input_dir}")
    
    return metadata_list

def scrape_angelone_support(base_url: str, output_dir: str) -> List[Dict[str, Any]]:
    """Scrape Angel One support website"""
    metadata_list = []
    visited_urls = set()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    def process_page(url: str) -> None:
        if url in visited_urls or not url.startswith(base_url):
            return
        
        visited_urls.add(url)
        
        try:
            # Fetch page content
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if not content:
                return
            
            # Clean text
            text = content.get_text(separator='\n', strip=True)
            
            # Save content
            filename = f"{len(metadata_list):04d}.txt"
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Add metadata
            metadata_list.append({
                'source': url,
                'type': 'webpage',
                'path': output_path
            })
            
            logger.info(f"Scraped {url}")
            
            # Find links to other pages
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                process_page(next_url)
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
    
    # Start scraping from base URL
    process_page(base_url)
    return metadata_list

# Configure logging

# Configure logging
logger = logging.getLogger(__name__)

def process_documents(pdf_directory: str, output_directory: str) -> None:
    """Process PDF and DOCX documents and create vector store"""
    try:
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        # Convert relative paths to absolute paths
        pdf_directory = os.path.abspath(pdf_directory)
        output_directory = os.path.abspath(output_directory)
        
        # Process documents
        metadata_list = process_document_directory(pdf_directory, output_directory)
        if not metadata_list:
            raise ValueError("No documents were processed successfully")
        logger.info(f"Processed {len(metadata_list)} documents")
        
        # Initialize document processor
        document_processor = DocumentProcessor(
            chunk_size=MODEL_CONFIG['chunk_size'],
            chunk_overlap=MODEL_CONFIG['chunk_overlap']
        )
        
        # Load and split documents
        documents = document_processor.load_and_split_documents(output_directory)
        if not documents:
            raise ValueError("No documents were loaded for processing")
        
        # Initialize vector store manager
        vector_store_manager = VectorStoreManager(
            google_api_key=GEMINI_API_KEY,
            persist_directory=VECTORSTORE_CONFIG['persist_directory']
        )
        
        # Create vector store
        vector_store_manager.create_chroma_db(documents)
        logger.info("Vector store created successfully")
        
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise

def scrape_website(base_url: str, output_directory: str) -> None:
    """Scrape website and create vector store"""
    try:
        # Scrape website
        metadata_list = scrape_angelone_support(base_url, output_directory)
        logger.info(f"Scraped {len(metadata_list)} pages")
        
        # Initialize document processor
        document_processor = DocumentProcessor(
            chunk_size=MODEL_CONFIG['chunk_size'],
            chunk_overlap=MODEL_CONFIG['chunk_overlap']
        )
        
        # Load and split documents
        documents = document_processor.load_and_split_documents(output_directory)
        
        # Initialize vector store manager
        vector_store_manager = VectorStoreManager(
            google_api_key=GEMINI_API_KEY,
            persist_directory=VECTORSTORE_CONFIG['persist_directory']
        )
        
        # Create vector store
        vector_store_manager.create_chroma_db(documents)
        logger.info("Vector store created successfully")
        
    except Exception as e:
        logger.error(f"Error scraping website: {str(e)}")
        raise

def process_all() -> None:
    """Process all documents and websites"""
    try:
        # Set up output directories
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        insurance_output_dir = os.path.join(base_dir, "backend", "data", "processed", "insurance")
        angelone_output_dir = os.path.join(base_dir, "backend", "data", "processed", "angelone")
        
        # Process insurance documents
        insurance_metadata = process_document_directory(
            input_dir=os.path.join(base_dir, "backend", "data", "Insurance"),
            output_dir=insurance_output_dir
        )
        
        # Scrape Angel One support website
        angelone_metadata = scrape_angelone_support(
            base_url="https://support.angelone.in",
            output_dir=angelone_output_dir
        )
        
        # Initialize document processor
        document_processor = DocumentProcessor(
            chunk_size=MODEL_CONFIG['chunk_size'],
            chunk_overlap=MODEL_CONFIG['chunk_overlap']
        )
        
        # Load and split documents
        insurance_docs = document_processor.load_and_split_documents(insurance_output_dir)
        angelone_docs = document_processor.load_and_split_documents(angelone_output_dir)
        
        all_documents = insurance_docs + angelone_docs
        
        # Initialize vector store manager
        vector_store_manager = VectorStoreManager(
            google_api_key=GEMINI_API_KEY,
            persist_directory=VECTORSTORE_CONFIG['persist_directory']
        )
        
        # Create vector store
        vector_store_manager.create_chroma_db(all_documents)
        
        logger.info(f"Processed {len(insurance_metadata)} insurance documents and {len(angelone_metadata)} Angel One pages")
        
    except Exception as e:
        logger.error(f"Error in process_all: {str(e)}")
        raise


class Retriever:
    def __init__(self, persist_directory: str, google_api_key: str):
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=google_api_key
            ),
            client_settings=chromadb.config.Settings(
                anonymized_telemetry=False,
                persist_directory=persist_directory,
                is_persistent=True
            )
        )
    
    async def get_relevant_documents(self, query: str, k: int = 4) -> List[Any]:
        """Retrieve relevant documents for a given query using similarity search"""
        try:
            documents = self.vector_store.similarity_search(query, k=k)
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise