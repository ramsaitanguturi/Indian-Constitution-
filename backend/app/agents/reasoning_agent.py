from typing import Dict, Any
from app.core.config import settings, get_llm
from app.core.logging import logger
from app.agents.state import AgentState

def generate_reasoning_local(state: AgentState) -> str:
    """
    Fallback reasoning generator for local/offline execution.
    Creates a high-quality constitutional analysis based on retrieved articles and cases.
    Identifies a Primary Article and Supporting Articles for multi-article reasoning.
    """
    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    issue = state.get("detected_legal_issue") or "Constitutional Protection"
    query = state.get("user_query")
    
    if not articles:
        return "No specific constitutional provisions were retrieved to perform legal analysis."
        
    primary = articles[0]
    supporting = articles[1:] if len(articles) > 1 else []
    best_case = cases[0] if cases else None
    
    art_num = primary.get("article_number", "")
    art_title = primary.get("title", "")
    clause = primary.get("clause")
    
    reasoning = (
        f"Under Indian Constitutional Law, this scenario relates to the category of '{issue}'.\n\n"
        f"1. Constitutional Foundation (Primary Article): The primary provision is Article {art_num} ({art_title})"
    )
    if clause:
        reasoning += f", specifically referencing clause/protection '{clause}'"
    reasoning += f". The text guarantees: '{primary.get('content', '')}'.\n"
    
    if supporting:
        reasoning += "\n2. Supporting Constitutional Provisions: "
        sub_texts = []
        for art in supporting[:2]:
            sub_clause_str = f" (Clause {art.get('clause')})" if art.get("clause") else ""
            sub_texts.append(f"Article {art.get('article_number')} ({art.get('title')}){sub_clause_str} - which states: '{art.get('content', '')}'")
        reasoning += " Additionally, this is connected to: " + "; and ".join(sub_texts) + ".\n"
    
    if best_case:
        reasoning += (
            f"\n3. Judicial Precedent: The landmark Supreme Court case {best_case.get('case_name')} "
            f"({best_case.get('citation')}) is highly relevant. In this case, the court held that: "
            f"'{best_case.get('summary', '')}'.\n\n"
            f"4. Legal Synthesis: The facts of the query ('{query}') present a potential conflict. "
            f"As established in {best_case.get('case_name')}, the state cannot execute arbitrary actions "
            f"that infringe upon the core rights guaranteed under Article {art_num} or supporting articles unless it satisfies "
            f"established constitutional limitations (such as the proportionality test or reasonable restrictions)."
        )
    else:
        reasoning += (
            f"\n3. Legal Synthesis: Any state or government action that infringes upon the core rights guaranteed "
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
    
    llm = get_llm(temperature=0.2)
    if llm:
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            import os
            
            # Load reasoning prompt from template file
            PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")
            prompt_path = os.path.join(PROMPTS_DIR, "reasoning_prompt.txt")
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    system_prompt_template = f.read()
            else:
                system_prompt_template = (
                    "You are an expert Indian Constitutional Law Reasoning Agent.\n"
                    "Your task is to connect the user's legal scenario with the retrieved constitutional articles and landmark cases.\n"
                    "Retrieved Articles:\n{articles_str}\n"
                    "Retrieved Landmark Cases:\n{cases_str}\n"
                    "User Scenario:\n{query}"
                )
            
            # Format retrieved materials for the LLM prompt
            articles_str = ""
            for idx, art in enumerate(articles, 1):
                articles_str += f"[{idx}] Article {art.get('article_number')}: {art.get('title')}\nContent: {art.get('content')}\n\n"
                
            cases_str = ""
            for idx, case in enumerate(cases, 1):
                cases_str += f"[{idx}] {case.get('case_name')} ({case.get('citation')})\nSummary: {case.get('summary')}\n\n"
                
            system_prompt = system_prompt_template.replace("{articles_str}", articles_str)
            system_prompt = system_prompt.replace("{cases_str}", cases_str)
            system_prompt = system_prompt.replace("{query}", query)
            
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
