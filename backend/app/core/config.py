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
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Production CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # App configuration to load from environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

def get_llm(temperature: float = 0.2, model_name: str = None):
    import os
    # Priority 1: Google API Key
    google_key = settings.GOOGLE_API_KEY or os.environ.get("GOOGLE_API_KEY")
    if google_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        target_model = model_name or settings.GEMINI_MODEL or "gemini-2.0-flash"
        return ChatGoogleGenerativeAI(
            model=target_model,
            google_api_key=google_key,
            temperature=temperature
        )
        
    # Priority 2: OpenRouter API Key as fallback (uses google/gemini-2.5-flash)
    openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if openrouter_key:
        from langchain_openai import ChatOpenAI
        # OpenRouter requires the full provider-prefixed model ID
        raw_model = model_name or settings.GEMINI_MODEL or "gemini-2.5-flash"
        if raw_model.startswith("google/"):
            target_model = raw_model
        else:
            # Map local model name to OpenRouter model slug
            openrouter_map = {
                "gemini-2.5-flash": "google/gemini-2.5-flash",
                "gemini-2.0-flash": "google/gemini-2.5-flash",
                "gemini-1.5-flash": "google/gemini-3.5-flash",
            }
            target_model = openrouter_map.get(raw_model, f"google/{raw_model}")
            
        return ChatOpenAI(
            model=target_model,
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=1024
        )
        
    return None

