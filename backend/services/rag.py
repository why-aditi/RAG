import logging
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
import google.generativeai as genai

from .document_processor import VectorStoreManager, Retriever
from config import GEMINI_API_KEY, VECTORSTORE_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

class RAGPipeline:
    """RAG Pipeline for question answering using Gemini and vector store retrieval"""
    
    def __init__(self, retriever: Retriever, google_api_key: str):
        """Initialize the RAG pipeline"""
        self.retriever = retriever
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        
    async def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using RAG"""
        # Retrieve relevant documents
        relevant_docs = await self.retriever.get_relevant_documents(question)
        
        if not relevant_docs:
            return {
                "answer": "I don't know.",
                "sources": []
            }
        
        # Construct prompt with retrieved context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"Based on the following context, please answer the question. If you cannot answer based on the context alone, say so.\n\nContext:\n{context}\n\nQuestion: {question}"
        
        # Generate response using Gemini
        response = self.model.generate_content(prompt)
        
        return {
            "answer": response.text,
            "sources": [{
                "content": doc.page_content,
                "metadata": doc.metadata
            } for doc in relevant_docs]
        }

# Global variables for RAG components
rag_pipeline = None

# Function to get RAG pipeline
async def get_rag_pipeline() -> RAGPipeline:
    """Get or initialize the RAG pipeline"""
    global rag_pipeline
    
    if rag_pipeline is None:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI API key not configured")
            
        # Initialize vector store manager
        vector_store_manager = VectorStoreManager(
            google_api_key=GEMINI_API_KEY,
            persist_directory=VECTORSTORE_CONFIG['persist_directory']
        )
        
        # Try to load existing vector store
        vectorstore = vector_store_manager.load_chroma_db()
        
        if vectorstore is None:
            raise HTTPException(
                status_code=404,
                detail="Vector store not found. Please process documents first."
            )
            
        # Initialize retriever and RAG pipeline
        retriever = Retriever(persist_directory=VECTORSTORE_CONFIG['persist_directory'], google_api_key=GEMINI_API_KEY)
        rag_pipeline = RAGPipeline(
            retriever=retriever,
            google_api_key=GEMINI_API_KEY
        )
        
    return rag_pipeline