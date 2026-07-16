from typing import Dict, Any
from app.services.rag_service import rag_service
from app.agents.state import AgentState
from app.schemas.chat import ArticleResponse
from app.core.logging import logger

def case_law_agent(state: AgentState) -> Dict[str, Any]:
    """
    Case Law Agent: Retrieves landmark Supreme Court judgments from ChromaDB.
    """
    logger.info("Running Case Law Agent...")
    query = state["user_query"]
    processed = state.get("processed_query")
    
    # Safely convert retrieved articles from state dictionaries back to Pydantic objects if present
    articles_data = state.get("retrieved_articles") or []
    retrieved_articles = [ArticleResponse(**art) for art in articles_data]
    
    category = state.get("detected_legal_issue")
    
    # Extract concept cases if available from state
    concepts = state.get("detected_concepts") or (processed.get("concept_info") if processed else None) or {}
    concept_cases = concepts.get("related_cases", [])
    
    # Retrieve case laws using the modular RAG service
    cases = rag_service.retrieve_cases(
        query, 
        retrieved_articles=retrieved_articles, 
        limit=3, 
        processed_query=processed, 
        category=category,
        concept_cases=concept_cases
    )
    
    # Serialize Pydantic objects to dictionaries for LangGraph state storage
    cases_data = [case.model_dump() for case in cases]
    
    logger.info(f"Case Law Agent retrieved {len(cases_data)} cases.")
    return {
        "retrieved_cases": cases_data
    }
