from typing import Dict, Any
from app.services.rag_service import rag_service
from app.agents.state import AgentState
from app.core.logging import logger

def constitution_agent(state: AgentState) -> Dict[str, Any]:
    """
    Constitution Agent: Retrieves relevant constitutional articles from ChromaDB.
    """
    logger.info("Running Constitution Agent...")
    query = state["user_query"]
    processed = state.get("processed_query")
    category = state.get("detected_legal_issue")
    
    # If the query is completely off-topic, skip article retrieval
    if category == "Non-Legal":
        logger.info("Constitution Agent: Query category indicates no constitutional retrieval needed. Returning empty list.")
        return {"retrieved_articles": []}
    
    # Extract concept articles if available from state
    concepts = state.get("detected_concepts") or (processed.get("concept_info") if processed else None) or {}
    concept_articles = concepts.get("related_articles", [])
    
    # Retrieve articles using the modular RAG service
    articles = rag_service.retrieve_articles(
        query, 
        limit=3, 
        processed_query=processed, 
        category=category,
        concept_articles=concept_articles
    )
    
    # Serialize Pydantic objects to dictionaries for LangGraph state storage
    articles_data = [art.model_dump() for art in articles]
    
    logger.info(f"Constitution Agent retrieved {len(articles_data)} articles.")
    return {
        "retrieved_articles": articles_data
    }
