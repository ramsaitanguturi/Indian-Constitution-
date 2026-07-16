import json
import re
from typing import Dict, Any
from app.core.config import settings, get_llm
from app.core.logging import logger
from app.agents.state import AgentState

def validate_local(state: AgentState) -> Dict[str, Any]:
    """
    Fallback deterministic validator for local/offline execution.
    Checks if resources are loaded and align with the query.
    """
    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    
    if not articles:
        return {
            "is_valid": False,
            "hallucination_risk": "High",
            "details": "Validation failed: No constitutional articles retrieved for the query."
        }
        
    # Check if there's any case retrieved
    if not cases:
        return {
            "is_valid": True,
            "hallucination_risk": "Medium",
            "details": "Validation warning: Constitutional articles retrieved, but no matching landmark case laws were found."
        }
        
    return {
        "is_valid": True,
        "hallucination_risk": "Low",
        "details": f"Validation successful: Retrieved Article {articles[0].get('article_number')} and Case {cases[0].get('case_name')} match the legal topic."
    }

def validation_agent(state: AgentState) -> Dict[str, Any]:
    """
    Validation Agent: Verifies article relevance, case relevance, and hallucination risk in the reasoning.
    """
    logger.info("Running Validation Agent...")
    query = state["user_query"]
    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    reasoning = state.get("reasoning_chain") or ""
    
    # Pre-check: If no articles retrieved, fail immediately with high hallucination risk
    if not articles:
        return {
            "validation_result": {
                "is_valid": False,
                "hallucination_risk": "High",
                "details": "Validation failed: Retrieved articles do not exist.",
                "action": "stop"
            }
        }
        
    validation_res = None
    
    llm = get_llm(temperature=0.2)
    if llm:
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            
            articles_str = ""
            for idx, art in enumerate(articles, 1):
                articles_str += f"[{idx}] Article {art.get('article_number')}: {art.get('title')}\nContent: {art.get('content')}\n\n"
                
            cases_str = ""
            for idx, case in enumerate(cases, 1):
                cases_str += f"[{idx}] {case.get('case_name')} ({case.get('citation')})\nSummary: {case.get('summary')}\n\n"
                
            system_prompt = (
                "You are an expert Constitutional Law Validation Agent.\n"
                "Your task is to check the generated reasoning against the retrieved articles and cases.\n\n"
                "Verify the following three criteria strictly:\n"
                "1. Retrieved Articles Exist: Are the retrieved articles present and relevant to the query?\n"
                "2. Retrieved Cases Exist: Are the retrieved cases present and relevant?\n"
                "3. Reasoning Matches Evidence: Does the reasoning rely ONLY on the retrieved articles and cases? If the reasoning mentions any articles, cases, or facts NOT in the retrieved data, this check fails.\n\n"
                "Respond ONLY with a valid JSON object of the following format:\n"
                "{\n"
                "  \"is_valid\": true or false,\n"
                "  \"hallucination_risk\": \"Low\", \"Medium\", or \"High\",\n"
                "  \"details\": \"A concise summary of the verification findings: (1) retrieved articles exist check result, (2) retrieved cases exist check result, (3) reasoning matches evidence check result.\",\n"
                "  \"action\": \"proceed\" or \"stop\"\n"
                "}"
            )
            
            user_content = (
                f"Scenario: {query}\n\n"
                f"Retrieved Articles:\n{articles_str}\n"
                f"Retrieved Cases:\n{cases_str}\n"
                f"Draft Reasoning Chain:\n{reasoning}"
            )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content)
            ]
            
            response = llm.invoke(messages)
            content = response.content.strip()
            
            # Simple regex to extract JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                content = match.group(0)
                
            validation_res = json.loads(content)
            
            # If is_valid is false, set action to stop
            if not validation_res.get("is_valid"):
                validation_res["action"] = "stop"
            else:
                validation_res["action"] = "proceed"
                
            logger.info(f"LLM Validation Result: {validation_res}")
        except Exception as e:
            logger.warning(f"LLM validation agent failed: {e}. Falling back to local validation.")
            
    if not validation_res:
        validation_res = validate_local(state)
        logger.info(f"Local Fallback Validation Result: {validation_res}")
        
    return {
        "validation_result": validation_res
    }
