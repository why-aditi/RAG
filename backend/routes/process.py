from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from services.document_processor import process_documents, scrape_website, process_all

router = APIRouter()

class ProcessDocumentsRequest(BaseModel):
    pdf_directory: str
    output_directory: str

class ScrapeWebsiteRequest(BaseModel):
    base_url: str
    output_directory: str

@router.post('/documents')
async def process_documents_endpoint(request: ProcessDocumentsRequest, background_tasks: BackgroundTasks):
    """Process PDF and DOCX documents and create vector store"""
    background_tasks.add_task(
        process_documents,
        request.pdf_directory,
        request.output_directory
    )
    return {"message": "Document processing started in background"}

@router.post('/website')
async def scrape_website_endpoint(request: ScrapeWebsiteRequest, background_tasks: BackgroundTasks):
    """Scrape Angel One support website and create vector store"""
    background_tasks.add_task(
        scrape_website,
        request.base_url,
        request.output_directory
    )
    return {"message": "Website scraping started in background"}

@router.post('/all')
async def process_all_endpoint(background_tasks: BackgroundTasks):
    """Process all documents and websites"""
    background_tasks.add_task(process_all)
    return {"message": "Processing all documents and websites started in background"}