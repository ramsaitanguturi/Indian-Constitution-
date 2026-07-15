from fastapi import APIRouter, HTTPException
from app.schemas.chat import QueryRequest, QueryResponse
from app.services.agent_service import agent_service
from app.core.logging import logger

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_constitution(payload: QueryRequest):
    """
    Search the Indian Constitution and landmark case laws using hierarchical RAG and LangGraph agent workflow.
    """
    try:
        response = agent_service.run_query(payload.query, limit=payload.limit)
        return response
    except Exception as e:
        logger.error(f"Error querying Agent service: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/search", response_model=QueryResponse)
def search_constitution(payload: QueryRequest):
    """
    Alias endpoint for query.
    """
    return query_constitution(payload)

