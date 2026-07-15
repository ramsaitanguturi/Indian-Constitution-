import json
import re
from typing import Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.agents.state import AgentState

def generate_verdict_local(state: AgentState) -> Dict[str, Any]:
    """
    Fallback deterministic verdict for local/offline execution.
    Synthesizes the verdict and formats the final markdown report.
    """
    # 1. Check if the router stopped the workflow
    val_res = state.get("validation_result") or {}
    if val_res.get("action") == "stop" or state.get("detected_legal_issue") == "Non-Legal":
        final_answer = (
            "# Indian Constitution Assistant\n\n"
            "**I'm sorry, but your query does not appear to be related to Indian Constitutional Law or legal rights.**\n\n"
            "Please ask a question regarding fundamental rights, constitutional articles, or landmark Supreme Court judgments."
        )
        return {
            "confidence_score": 0.0,
            "final_answer": final_answer,
            "verdict": "Query classified as non-legal or off-topic. No constitutional verdict predicted."
        }

    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    reasoning = state.get("reasoning_chain") or ""
    
    if not articles:
        return {
            "confidence_score": 0.3,
            "verdict": "Inconclusive outcome due to lack of constitutional provisions.",
            "final_answer": "# Legal Analysis\n\nNo relevant constitutional articles were found to synthesize a verdict."
        }
        
    best_art = articles[0]
    best_case = cases[0] if cases else None
    
    art_num = best_art.get("article_number", "")
    art_title = best_art.get("title", "")
    
    # Predict verdict
    verdict = f"State or government actions violating the criteria set under Article {art_num} ({art_title}) are likely to be declared unconstitutional."
    
    # Calculate confidence based on similarity score of article and validation
    sim_score = best_art.get("similarity_score", 0.8)
    confidence = 0.9 if sim_score > 0.6 and best_case else 0.7
    
    # Format the final markdown report
    md_report = f"# Constitutional Analysis Report\n\n"
    md_report += f"## ⚖️ User Query\n> {state.get('user_query')}\n\n"
    
    md_report += f"## 📖 Relevant Constitutional Provisions\n"
    for art in articles:
        clause_str = f" (Clause {art.get('clause')})" if art.get("clause") else ""
        md_report += f"- **Article {art.get('article_number')}: {art.get('title')}{clause_str}**\n"
        md_report += f"  > {art.get('content')}\n\n"
        
    if cases:
        md_report += f"## 🏛️ Landmark Case Jurisprudence\n"
        for c in cases:
            md_report += f"- **{c.get('case_name')} ({c.get('citation')})**\n"
            md_report += f"  > *Summary:* {c.get('summary')}\n\n"
            
    md_report += f"## 🧠 Legal Reasoning & Analysis\n{reasoning}\n\n"
    md_report += f"## 🎯 Predicted Constitutional Outcome / Verdict\n**{verdict}**\n\n"
    md_report += f"## 📊 Confidence Level: {'High' if confidence >= 0.8 else 'Medium'} ({confidence * 100:.1f}%)\n"
    
    return {
        "confidence_score": confidence,
        "final_answer": md_report,
        "verdict": verdict
    }

def verdict_agent(state: AgentState) -> Dict[str, Any]:
    """
    Verdict Agent: Formulates the final verdict, confidence score, and compiles the final markdown report.
    """
    logger.info("Running Verdict Agent...")
    
    verdict_data = None
    
    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import SystemMessage, HumanMessage
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2
            )
            
            # If off-topic, generate a clean stop verdict
            val_res = state.get("validation_result") or {}
            if val_res.get("action") == "stop" or state.get("detected_legal_issue") == "Non-Legal":
                system_prompt = (
                    "You are a helpful Indian Constitutional Law AI Assistant.\n"
                    "The user query is off-topic or not related to constitutional law.\n"
                    "Respond politely explaining that you specialize in Indian Constitutional Law queries.\n"
                    "Respond ONLY in JSON format:\n"
                    "{\n"
                    "  \"verdict\": \"Query is off-topic.\",\n"
                    "  \"confidence_score\": 0.0,\n"
                    "  \"final_answer\": \"Markdown response explaining that the query is off-topic\"\n"
                    "}"
                )
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Query: {state['user_query']}")
                ]
                response = llm.invoke(messages)
                content = response.content.strip()
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    content = match.group(0)
                verdict_data = json.loads(content)
            else:
                articles = state.get("retrieved_articles") or []
                cases = state.get("retrieved_cases") or []
                reasoning = state.get("reasoning_chain") or ""
                validation = state.get("validation_result") or {}
                
                articles_str = ""
                for idx, art in enumerate(articles, 1):
                    articles_str += f"[{idx}] Article {art.get('article_number')}: {art.get('title')}\nContent: {art.get('content')}\n\n"
                    
                cases_str = ""
                for idx, case in enumerate(cases, 1):
                    cases_str += f"[{idx}] {case.get('case_name')} ({case.get('citation')})\nSummary: {case.get('summary')}\n\n"
                
                system_prompt = (
                    "You are an expert Constitutional Supreme Court Verdict Agent.\n"
                    "Review the legal scenario, reasoning chain, and validation results. Predict the possible constitutional outcome (verdict) based on established legal doctrines and precedents.\n"
                    "Assign a confidence score (0.0 to 1.0) based on relevance of sources and validation feedback.\n"
                    "Generate a comprehensive, beautifully structured markdown report (final_answer) presenting the analysis, citations, reasoning, and verdict.\n\n"
                    "Respond ONLY in JSON format:\n"
                    "{\n"
                    "  \"verdict\": \"Clear outcome statement\",\n"
                    "  \"confidence_score\": 0.9,\n"
                    "  \"final_answer\": \"# Detailed Markdown Report\\n\\n...\"\n"
                    "}"
                )
                
                user_content = (
                    f"Scenario: {state['user_query']}\n\n"
                    f"Retrieved Articles:\n{articles_str}\n"
                    f"Retrieved Cases:\n{cases_str}\n"
                    f"Legal Reasoning:\n{reasoning}\n"
                    f"Validation Result:\n{json.dumps(validation)}"
                )
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_content)
                ]
                
                response = llm.invoke(messages)
                content = response.content.strip()
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    content = match.group(0)
                verdict_data = json.loads(content)
                logger.info("LLM Verdict and report generated.")
        except Exception as e:
            logger.warning(f"LLM verdict agent failed: {e}. Falling back to local verdict.")
            
    if not verdict_data:
        verdict_data = generate_verdict_local(state)
        logger.info("Local Fallback Verdict and report generated.")
        
    return {
        "confidence_score": verdict_data.get("confidence_score", 0.0),
        "final_answer": verdict_data.get("final_answer", ""),
        "verdict": verdict_data.get("verdict", "")
    }
