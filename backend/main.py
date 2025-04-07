import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import API_CONFIG, CORS_CONFIG, LOGGING_CONFIG
from routes import api_router

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG['title'],
    description=API_CONFIG['description'],
    version=API_CONFIG['version'],
    docs_url=API_CONFIG['docs_url'],
    redoc_url=API_CONFIG['redoc_url']
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG['allow_origins'],
    allow_credentials=CORS_CONFIG['allow_credentials'],
    allow_methods=CORS_CONFIG['allow_methods'],
    allow_headers=CORS_CONFIG['allow_headers']
)

# Include API routes
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "RAG Customer Support Chatbot API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
