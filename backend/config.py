import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# API Configuration
API_CONFIG = {
    'title': 'RAG Customer Support Chatbot API',
    'description': 'API for RAG-based customer support chatbot',
    'version': '1.0.0',
    'docs_url': '/docs',
    'redoc_url': '/redoc'
}

# CORS Configuration
CORS_CONFIG = {
    'allow_origins': ['*'],
    'allow_credentials': True,
    'allow_methods': ['*'],
    'allow_headers': ['*']
}

# Model Configuration
MODEL_CONFIG = {
    'chunk_size': 1000,
    'chunk_overlap': 200,
    'model_name': 'models/gemini-2.0-flash',
    'temperature': 0.7,
    'top_k': 5
}

# Vector Store Configuration
VECTORSTORE_CONFIG = {
    'persist_directory': str(PROCESSED_DIR / 'chroma_db')
}

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}