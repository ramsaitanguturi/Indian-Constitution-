from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.db.chroma import db_manager
from app.schemas.chat import QueryRequest, QueryResponse
from app.services.agent_service import agent_service
from app.core.logging import logger

# Setup logging on startup
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On application startup, check if ChromaDB is empty and automatically run
    the ingestion pipeline to populate collections if needed.
    """
    try:
        parents_col = db_manager.get_parents_collection()
        children_col = db_manager.get_children_collection()
        cases_col = db_manager.get_cases_collection()
        
        parents_count = parents_col.count()
        children_count = children_col.count()
        cases_count = cases_col.count()
        
        if parents_count == 0 and children_count == 0 and cases_count == 0:
            logger.info("Empty database detected, running ingestion")
            # Dynamically import scripts.ingest_data to optimize memory footprint
            from scripts.ingest_data import ingest_constitution, ingest_cases
            ingest_constitution()
            ingest_cases()
            logger.info("Ingestion completed successfully during startup!")
            
            # Close client to flush HNSW index to disk, then reset singleton
            if db_manager._client:
                logger.info("Flushing database changes to disk...")
                db_manager._client.close()
                db_manager._client = None
                db_manager._embedding_function = None
        else:
            logger.info("Existing ChromaDB found, skipping ingestion")
    except Exception as e:
        logger.error(f"Error during database initialization check: {e}", exc_info=True)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the Constitution RAG Agent, delivering constitutional analysis and verdict predictions.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Parse CORS Origins configuration
origins = settings.BACKEND_CORS_ORIGINS
if isinstance(origins, str):
    try:
        origins = json.loads(origins)
    except Exception:
        origins = [o.strip() for o in origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "docs_url": "/docs",
        "health_check": "/health",
        "system_info": "/system-info"
    }

@app.get("/health")
def health_check():
    """
    Production-ready health check verifying live database connection.
    """
    try:
        parents_count = db_manager.get_parents_collection().count()
        return {
            "status": "healthy",
            "database": f"ChromaDB connection successful. Parent articles index count: {parents_count}"
        }
    except Exception as e:
        logger.error(f"Health check failed: database connection error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unhealthy system: database connection failed: {str(e)}"
        )

@app.get("/system-info")
def system_info():
    """
    Retrieve production environment details and indexing statistics.
    """
    try:
        parents_count = db_manager.get_parents_collection().count()
        children_count = db_manager.get_children_collection().count()
        cases_count = db_manager.get_cases_collection().count()
        database_status = "connected"
    except Exception as e:
        logger.error(f"Error fetching collections count: {e}")
        parents_count = children_count = cases_count = -1
        database_status = f"error: {str(e)}"

    return {
        "project_name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "embedding_provider": settings.EMBEDDING_PROVIDER,
        "gemini_model": settings.GEMINI_MODEL,
        "database": {
            "status": database_status,
            "articles_count": parents_count,
            "clauses_count": children_count,
            "cases_count": cases_count
        }
    }

@app.post("/query", response_model=QueryResponse)
def query_root(payload: QueryRequest):
    """
    Root level alias endpoint for querying the legal agents RAG system.
    """
    try:
        return agent_service.run_query(payload.query, limit=payload.limit)
    except Exception as e:
        logger.error(f"Error querying Agent service at root level: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/query/stream")
def query_root_stream(payload: QueryRequest):
    """
    Root level alias endpoint for streaming search of the Indian Constitution and landmark case laws.
    """
    def event_generator():
        try:
            for event in agent_service.run_query_stream(payload.query, limit=payload.limit):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming query at root level: {e}", exc_info=True)
            yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
