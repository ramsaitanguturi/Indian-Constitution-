from typing import Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.agents.state import AgentState

def generate_reasoning_local(state: AgentState) -> str:
    """
    Fallback reasoning generator for local/offline execution.
    Creates a high-quality constitutional analysis based on retrieved articles and cases.
    """
    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    issue = state.get("detected_legal_issue") or "Constitutional Protection"
    query = state.get("user_query")
    
    if not articles:
        return "No specific constitutional provisions were retrieved to perform legal analysis."
        
    best_art = articles[0]
    best_case = cases[0] if cases else None
    
    art_num = best_art.get("article_number", "")
    art_title = best_art.get("title", "")
    clause = best_art.get("clause")
    
    reasoning = (
        f"Under Indian Constitutional Law, this scenario relates to the category of '{issue}'.\n"
        f"1. Constitutional Foundation: The issue falls under the scope of Article {art_num} ({art_title})"
    )
    if clause:
        reasoning += f", specifically referencing clause/protection '{clause}'"
    reasoning += f". The text guarantees: '{best_art.get('content', '')}'.\n"
    
    if best_case:
        reasoning += (
            f"2. Judicial Precedent: The landmark Supreme Court case {best_case.get('case_name')} "
            f"({best_case.get('citation')}) is highly relevant. In this case, the court held that: "
            f"'{best_case.get('summary', '')}'.\n"
            f"3. Legal Synthesis: The facts of the query ('{query}') present a potential conflict. "
            f"As established in {best_case.get('case_name')}, the state cannot execute arbitrary actions "
            f"that infringe upon the core rights guaranteed under Article {art_num} unless it satisfies "
            f"established constitutional limitations (such as the proportionality test or reasonable restrictions)."
        )
    else:
        reasoning += (
            f"2. Legal Synthesis: Any state or government action that infringes upon the core rights guaranteed "
            f"under Article {art_num} must be justified by law, serve a legitimate state interest, and be proportional."
        )
        
    return reasoning

def reasoning_agent(state: AgentState) -> Dict[str, Any]:
    """
    Reasoning Agent: Connects the user scenario, retrieved articles, and landmark cases to build a reasoning chain.
    """
    logger.info("Running Reasoning Agent...")
    query = state["user_query"]
    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    
    reasoning_chain = None
    
    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import SystemMessage, HumanMessage
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2
            )
            
            # Format retrieved materials for the LLM prompt
            articles_str = ""
            for idx, art in enumerate(articles, 1):
                articles_str += f"[{idx}] Article {art.get('article_number')}: {art.get('title')}\nContent: {art.get('content')}\n\n"
                
            cases_str = ""
            for idx, case in enumerate(cases, 1):
                cases_str += f"[{idx}] {case.get('case_name')} ({case.get('citation')})\nSummary: {case.get('summary')}\n\n"
                
            system_prompt = (
                "You are an expert Constitutional Law Reasoning Agent.\n"
                "Your task is to connect the user's legal scenario with the retrieved constitutional articles and landmark cases.\n"
                "Construct a step-by-step legal reasoning chain. Explain the legal connection, the constitutional principles involved, and how the cited cases apply to the scenario.\n"
                "Rely strictly on the provided retrieved text and do not assume or hallucinate legal facts.\n\n"
                f"Retrieved Articles:\n{articles_str}\n"
                f"Retrieved Landmark Cases:\n{cases_str}"
            )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Scenario: {query}")
            ]
            
            response = llm.invoke(messages)
            reasoning_chain = response.content.strip()
            logger.info("LLM Reasoning Chain generated successfully.")
        except Exception as e:
            logger.warning(f"LLM reasoning agent failed: {e}. Falling back to rule-based reasoning.")
            
    if not reasoning_chain:
        reasoning_chain = generate_reasoning_local(state)
        logger.info("Local Fallback Reasoning Chain generated.")
        
    return {
        "reasoning_chain": reasoning_chain
    }
