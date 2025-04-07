import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

from services.rag import get_rag_pipeline
from config import GEMINI_API_KEY

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Dict[str, Any]]
    confidence: str

@router.post('', response_model=ChatResponse)
async def chat(request: ChatRequest, rag_pipeline = Depends(get_rag_pipeline)):
    """Chat with the RAG pipeline"""
    try:
        result = await rag_pipeline.answer_question(request.question)
        return ChatResponse(
            answer=result['answer'],
            sources=result['sources'],
            confidence='high' if result['sources'] else 'low'
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat request: {str(e)}")