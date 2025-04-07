from fastapi import APIRouter

from .chat import router as chat_router
from .process import router as process_router

api_router = APIRouter()

api_router.include_router(chat_router, prefix='/chat', tags=['chat'])
api_router.include_router(process_router, prefix='/process', tags=['process'])