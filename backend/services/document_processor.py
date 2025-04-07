import logging
import os
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import TextLoader
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
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                try:
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    logger.error(f"Error loading {filename}: {str(e)}")
        
        # Split documents into chunks
        return self.text_splitter.split_documents(documents)

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
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{Path(filename).stem}.txt")
            
            try:
                # Open PDF document
                doc = fitz.open(input_path)
                
                # Extract text from each page
                text = ""
                for page in doc:
                    text += page.get_text()
                
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
        # Process documents
        metadata_list = process_document_directory(pdf_directory, output_directory)
        logger.info(f"Processed {len(metadata_list)} documents")
        
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
        # Process insurance documents
        insurance_metadata = process_document_directory(
            "Insurance PDFs",
            "backend/data/insurance_docs"
        )
        
        # Scrape Angel One support website
        angelone_metadata = scrape_angelone_support(
            "https://support.angelone.in",
            "backend/data/angelone_support"
        )
        
        # Initialize document processor
        document_processor = DocumentProcessor(
            chunk_size=MODEL_CONFIG['chunk_size'],
            chunk_overlap=MODEL_CONFIG['chunk_overlap']
        )
        
        # Load and split documents
        insurance_docs = document_processor.load_and_split_documents("backend/data/insurance_docs")
        angelone_docs = document_processor.load_and_split_documents("backend/data/angelone_support")
        
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