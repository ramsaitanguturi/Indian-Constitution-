import os
import threading
import chromadb
from app.core.config import settings
from app.core.logging import logger

class ChromaDBManager:
    def __init__(self):
        logger.info(f"Initializing ChromaDB persistent manager at: {settings.CHROMADB_DIR}")
        os.makedirs(settings.CHROMADB_DIR, exist_ok=True)
        self._local = threading.local()

    def _get_client_and_embedding(self):
        """
        Retrieves or creates the thread-local PersistentClient and embedding function.
        """
        if not hasattr(self._local, "client"):
            logger.info(f"Creating new ChromaDB PersistentClient for thread {threading.get_ident()}")
            self._local.client = chromadb.PersistentClient(path=settings.CHROMADB_DIR)
            self._local.embedding_function = self._get_embedding_function()
        return self._local.client, self._local.embedding_function

    def _get_embedding_function(self):
        """
        Dynamically load embedding function based on configuration.
        Falls back to local SentenceTransformers or built-in ONNX MiniLM
        if dependencies are missing.
        """
        if settings.EMBEDDING_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            try:
                from chromadb.utils import embedding_functions
                logger.info(f"Using OpenAI Embeddings model: {settings.OPENAI_EMBEDDING_MODEL}")
                return embedding_functions.OpenAIEmbeddingFunction(
                    api_key=settings.OPENAI_API_KEY,
                    model_name=settings.OPENAI_EMBEDDING_MODEL
                )
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI Embeddings: {e}. Falling back to local.")
        
        try:
            from chromadb.utils import embedding_functions
            logger.info(f"Attempting to use SentenceTransformer: {settings.LOCAL_EMBEDDING_MODEL}")
            return embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.LOCAL_EMBEDDING_MODEL
            )
        except Exception as e:
            logger.warning(f"SentenceTransformers failed to load: {e}. Falling back to built-in ONNX MiniLM.")
            from chromadb.utils import embedding_functions
            return embedding_functions.ONNXMiniLM_L6_V2()

    def get_collection(self, name: str):
        """
        Retrieve or create a collection with the thread-local client and embedding function.
        """
        client, embedding_fn = self._get_client_and_embedding()
        return client.get_or_create_collection(
            name=name,
            embedding_function=embedding_fn
        )

    def get_parents_collection(self):
        return self.get_collection("constitution_parents")

    def get_children_collection(self):
        return self.get_collection("constitution_children")

    def get_cases_collection(self):
        return self.get_collection("case_laws")

# Global DB manager instance
db_manager = ChromaDBManager()
