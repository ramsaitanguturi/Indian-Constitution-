from typing import List, Dict, Any
from app.agents.workflow import agent_workflow
from app.schemas.chat import QueryResponse, ArticleResponse, CaseResponse
from app.core.logging import logger

class AgentService:
    def run_query(self, query_text: str, limit: int = 3) -> QueryResponse:
        """
        Executes the LangGraph Agentic RAG workflow.
        """
        logger.info(f"Invoking LangGraph workflow for query: '{query_text}'")
        
        # Initialize state with all requested keys
        initial_state = {
            "user_query": query_text,
            "processed_query": {},
            "detected_legal_issue": "",
            "retrieved_articles": [],
            "retrieved_cases": [],
            "reasoning_chain": "",
            "validation_result": {},
            "confidence_score": 0.0,
            "final_answer": ""
        }
        
        # Run workflow
        final_state = agent_workflow.invoke(initial_state)
        
        # Deserialize retrieve articles and cases
        articles_data = final_state.get("retrieved_articles") or []
        cases_data = final_state.get("retrieved_cases") or []
        
        articles = [ArticleResponse(**art) for art in articles_data]
        cases = [CaseResponse(**case) for case in cases_data]
        
        # Convert numeric confidence score to string (e.g. 'High', 'Medium', 'Low')
        conf_score = final_state.get("confidence_score", 0.0)
        if conf_score >= 0.8:
            confidence_str = "High"
        elif conf_score >= 0.5:
            confidence_str = "Medium"
        else:
            confidence_str = "Low"
            
        # Get verdict outcome. If verdict is not a top-level key or is empty, extract from final_answer
        verdict = final_state.get("verdict")
        if not verdict:
            # Fallback to checking final_answer
            final_ans = final_state.get("final_answer", "")
            # If final_answer is a report, let's extract the verdict or use the report itself
            verdict = final_ans
            
        logger.info("LangGraph workflow execution completed successfully.")
        return QueryResponse(
            question=final_state.get("user_query", query_text),
            articles=articles,
            cases=cases,
            reasoning=final_state.get("reasoning_chain"),
            verdict=verdict,
            confidence=confidence_str,
            validation_result=final_state.get("validation_result")
        )

agent_service = AgentService()
