# RAG-Based Customer Support Chatbot

A modern customer support chatbot powered by Retrieval-Augmented Generation (RAG) technology. This project combines web scraping, document processing, and advanced language models to provide accurate, source-truthful responses for customer inquiries.

## Features

- Web scraping of Angel One support pages
- PDF parsing for insurance documentation
- Vector-based retrieval system
- Source-truthful responses
- User-friendly React frontend
- FastAPI backend

## Project Structure

```
├── frontend/           # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   └── assets/
│   └── public/
├── backend/           # FastAPI backend
│   ├── data/
│   ├── routes/
│   ├── services/
│   └── main.py
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with necessary environment variables:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   python main.py
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

## Dependencies

### Frontend

- React
- Vite
- Axios
- TailwindCSS

### Backend

- FastAPI
- ChromaDB
- OpenAI
- Python-dotenv
- BeautifulSoup4
- PyPDF2

## Development

1. Data Collection

   - Web scraping from Angel One support pages
   - PDF parsing of insurance documentation

2. Preprocessing

   - Content chunking
   - Text cleaning
   - Metadata extraction

3. Vector Store

   - Embedding generation
   - ChromaDB integration

4. RAG Pipeline
   - Query processing
   - Context retrieval
   - Response generation

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
