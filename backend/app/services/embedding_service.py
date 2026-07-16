import threading
from app.core.config import settings
from app.core.logging import logger

try:
    from chromadb import EmbeddingFunction, Documents, Embeddings
except ImportError:
    # Fallback/stub definitions in case chromadb is not loaded/installed in current environment
    class EmbeddingFunction:
        pass
    Documents = list
    Embeddings = list

# Global cached model and lock to ensure thread safety
_model_lock = threading.Lock()
_cached_model = None

def get_embedding_model():
    """
    Returns the loaded SentenceTransformer model (singleton).
    Loads it lazily on the first request.
    """
    global _cached_model
    if _cached_model is None:
        with _model_lock:
            if _cached_model is None:
                logger.info(f"Loading SentenceTransformer model: {settings.LOCAL_EMBEDDING_MODEL} (lazily)...")
                try:
                    from sentence_transformers import SentenceTransformer
                    _cached_model = SentenceTransformer(settings.LOCAL_EMBEDDING_MODEL)
                    logger.info("SentenceTransformer model successfully loaded.")
                except Exception as e:
                    logger.error(f"Failed to load SentenceTransformer model: {e}")
                    raise e
    return _cached_model

class LazySentenceTransformerEmbeddingFunction(EmbeddingFunction):
    """
    A custom ChromaDB EmbeddingFunction that loads the SentenceTransformer model
    only when the first embedding request is processed, and uses a shared singleton
    to optimize memory across threads.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    @staticmethod
    def name() -> str:
        return "sentence_transformer"

    def __call__(self, input: Documents) -> Embeddings:
        # Load model lazily
        model = get_embedding_model()
        
        # Convert input (which could be chromadb Documents) to list of strings
        texts = list(input)
        
        # Encode documents
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
