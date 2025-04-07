from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

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
        result = rag_pipeline.chat(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))