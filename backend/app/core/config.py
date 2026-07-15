import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Constitution RAG API"
    API_V1_STR: str = "/api/v1"
    
    # ChromaDB Configuration
    # Store relative to backend folder or absolute
    CHROMADB_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "chroma")
    
    # Embedding Configuration
    # Supported: "local" (SentenceTransformers) or "openai"
    EMBEDDING_PROVIDER: str = "local"
    
    # Local Embedding Model (SentenceTransformers)
    LOCAL_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # OpenAI Embedding Model
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # OpenAI API Key (optional for Phase 1 if using local embeddings)
    OPENAI_API_KEY: Optional[str] = None

    # Google API Key (for Gemini LLM)
    GOOGLE_API_KEY: Optional[str] = None

    # App configuration to load from environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
