# RAG-Based Customer Support Chatbot

A modern chatbot system built using Retrieval-Augmented Generation (RAG) architecture, designed to provide intelligent customer support by leveraging document processing and vector search capabilities.

## Features

- Document Processing Pipeline
  - PDF document processing
  - Web scraping support
  - Text chunking and vectorization
- Vector Store Management
  - ChromaDB integration
  - Google AI embeddings
  - Efficient document retrieval
- Interactive Chat Interface
  - Real-time responses
  - Context-aware conversations
  - Modern React-based UI

## Project Structure

```
├── frontend/           # React + Vite frontend
│   ├── src/           # Source code
│   │   ├── components/# React components
│   │   ├── assets/    # Static assets
│   │   └── App.jsx    # Main application component
│   ├── public/        # Public assets
│   └── package.json   # Frontend dependencies
├── backend/           # FastAPI backend
│   ├── data/         # Data storage
│   │   ├── Insurance/# Insurance documents
│   │   └── processed/# Processed documents
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   └── main.py       # Application entry point
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Google AI API key

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   - Create a `config.py` file with your Google AI API key
   - Set up vector store configuration

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

### Document Processing

1. Place your PDF documents in the `backend/data/Insurance/` directory
2. The system supports:
   - PDF document processing
   - Web scraping from specified URLs
   - Automatic text chunking and vectorization

### Vector Store Management

- Documents are automatically processed and stored in ChromaDB
- The system uses Google AI embeddings for vector representation
- Efficient similarity search for relevant document retrieval

### Chat Interface

1. Access the chat interface at `http://localhost:5173`
2. Enter your query in the chat input
3. The system will:
   - Retrieve relevant documents
   - Generate context-aware responses
   - Maintain conversation history

## API Endpoints

- `POST /chat`: Send chat messages and receive responses
- `POST /process`: Trigger document processing
