from typing import List, Dict, Any
from app.agents.workflow import agent_workflow
from app.schemas.chat import QueryResponse, ArticleResponse, CaseResponse, CitationResponse
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
            "final_answer": "",
            "verdict_data": None
        }
        
        # Run workflow
        final_state = agent_workflow.invoke(initial_state)
        
        logger.info("LangGraph workflow execution completed successfully.")
        return self._serialize_state(final_state, query_text)

    def _serialize_state(self, final_state: Dict[str, Any], query_text: str) -> QueryResponse:
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
            
        # Extract strict response fields
        verdict_data = final_state.get("verdict_data") or {}
        issue = verdict_data.get("issue") or final_state.get("detected_legal_issue") or "Constitutional Protection"
        
        # Build constitutional articles citations
        constitutional_articles = []
        if verdict_data.get("constitutional_articles"):
            for art in verdict_data["constitutional_articles"]:
                constitutional_articles.append(CitationResponse(
                    name=art.get("name") or "",
                    year=art.get("year") or "1950",
                    relevance_explanation=art.get("relevance_explanation") or ""
                ))
        else:
            # fallback from retrieved_articles
            for art in articles:
                constitutional_articles.append(CitationResponse(
                    name=f"Article {art.article_number}: {art.title}",
                    year="1950",
                    relevance_explanation="Relevant article retrieved for the scenario."
                ))
                
        # Build case laws citations
        case_laws = []
        if verdict_data.get("case_laws"):
            for c in verdict_data["case_laws"]:
                case_laws.append(CitationResponse(
                    name=c.get("name") or "",
                    year=c.get("year") or "N/A",
                    relevance_explanation=c.get("relevance_explanation") or ""
                ))
        else:
            # fallback from retrieved_cases
            for c in cases:
                case_laws.append(CitationResponse(
                    name=c.case_name,
                    year="N/A",
                    relevance_explanation="Relevant case law retrieved for the scenario."
                ))
                
        legal_reasoning = verdict_data.get("legal_reasoning") or final_state.get("reasoning_chain")
        arguments_for = verdict_data.get("arguments_for") or "The state action infringes upon constitutional rights."
        arguments_against = verdict_data.get("arguments_against") or "The state may argue reasonable restrictions apply."
        possible_verdict = verdict_data.get("possible_verdict") or verdict
            
        return QueryResponse(
            question=final_state.get("user_query", query_text),
            articles=articles,
            cases=cases,
            reasoning=final_state.get("reasoning_chain"),
            verdict=verdict,
            confidence=confidence_str,
            validation_result=final_state.get("validation_result"),
            issue=issue,
            constitutional_articles=constitutional_articles,
            case_laws=case_laws,
            legal_reasoning=legal_reasoning,
            arguments_for=arguments_for,
            arguments_against=arguments_against,
            possible_verdict=possible_verdict
        )

    def run_query_stream(self, query_text: str, limit: int = 3):
        """
        Executes the LangGraph Agentic RAG workflow and yields progress events.
        """
        logger.info(f"Invoking LangGraph streaming workflow for query: '{query_text}'")
        
        initial_state = {
            "user_query": query_text,
            "processed_query": {},
            "detected_legal_issue": "",
            "retrieved_articles": [],
            "retrieved_cases": [],
            "reasoning_chain": "",
            "validation_result": {},
            "confidence_score": 0.0,
            "final_answer": "",
            "verdict_data": None
        }
        
        # Yield initial status
        yield {"event": "status", "node": "router", "message": "Router running..."}
        
        final_state = initial_state.copy()
        
        for event in agent_workflow.stream(initial_state):
            for node_name, state_update in event.items():
                if state_update and isinstance(state_update, dict):
                    final_state.update(state_update)
                
                # Check which node completed and yield the next state notification
                if node_name == "router":
                    val_res = final_state.get("validation_result") or {}
                    if val_res.get("action") == "stop" or final_state.get("detected_legal_issue") == "Non-Legal":
                        yield {"event": "status", "node": "verdict", "message": "Formulating final verdict..."}
                    else:
                        yield {"event": "status", "node": "constitution_agent", "message": "Searching Constitution..."}
                elif node_name == "constitution_agent":
                    yield {"event": "status", "node": "case_law_agent", "message": "Finding judgments..."}
                elif node_name == "case_law_agent":
                    yield {"event": "status", "node": "reasoning_agent", "message": "Generating reasoning..."}
                elif node_name == "reasoning_agent":
                    yield {"event": "status", "node": "validation_agent", "message": "Validating answer..."}
                elif node_name == "validation_agent":
                    yield {"event": "status", "node": "verdict_agent", "message": "Formulating final verdict..."}
        
        # Once stream finishes, serialize the final state to get the full QueryResponse
        response = self._serialize_state(final_state, query_text)
        yield {"event": "final_result", "data": response.model_dump()}

agent_service = AgentService()
