import json
import re
import os
from typing import Dict, Any
from app.core.config import settings, get_llm
from app.core.logging import logger
from app.agents.state import AgentState


def _parse_json_robust(content: str) -> dict:
    """
    Attempt to parse JSON from LLM output.
    Handles: markdown fences, trailing commas, truncated output.
    """
    # 1. Strip markdown fences
    content = content.strip()
    content = re.sub(r'^```(?:json)?\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*```$', '', content)
    content = content.strip()

    # 2. Extract JSON object (greedy match, innermost brace pair)
    match = re.search(r'(\{.*\})', content, re.DOTALL)
    if match:
        content = match.group(1)

    # 3. Try strict parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 4. Remove trailing commas before } or ]
    cleaned = re.sub(r',\s*([}\]])', r'\1', content)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 5. Attempt to close a truncated JSON by removing the last incomplete key-value
    # Strip trailing partial field (ends mid-string or mid-value)
    truncated = re.sub(r',?\s*"[^"]*"\s*:\s*[^,}\]]*$', '', cleaned).strip()
    if not truncated.endswith('}'):
        truncated += '}'
    try:
        return json.loads(truncated)
    except json.JSONDecodeError:
        pass

    # 6. Last resort: raise to let caller handle
    raise ValueError(f"Could not parse JSON from LLM output: {content[:200]}...")

def generate_verdict_local(state: AgentState) -> Dict[str, Any]:
    """
    Fallback deterministic verdict for local/offline execution.
    Synthesizes the verdict and formats the final markdown report.
    Checks retrieval confidence and formats Primary vs. Supporting articles.
    """
    # 1. Check if the router stopped the workflow
    val_res = state.get("validation_result") or {}
    category = state.get("detected_legal_issue") or state.get("category")
    if val_res.get("action") == "stop" or category == "Non-Legal":
        verdict_data = {
            "issue": "Non-Legal / Off-Topic",
            "constitutional_articles": [],
            "case_laws": [],
            "legal_reasoning": "The query is off-topic or not related to constitutional law.",
            "arguments_for": "N/A",
            "arguments_against": "N/A",
            "possible_verdict": "Relevant constitutional provisions could not be confidently identified.",
            "confidence": "Low"
        }
        return {
            "confidence_score": 0.0,
            "final_answer": "Relevant constitutional provisions could not be confidently identified.",
            "verdict": "Relevant constitutional provisions could not be confidently identified.",
            "verdict_data": verdict_data
        }

    articles = state.get("retrieved_articles") or []
    cases = state.get("retrieved_cases") or []
    reasoning = state.get("reasoning_chain") or ""
    
    # Check if we have insufficient knowledge (no articles, low similarity)
    top_score = articles[0].get("similarity_score", 0.0) if articles else 0.0
    insufficient = (not articles) or (top_score < 0.4)
    
    if insufficient:
        verdict_data = {
            "issue": category or "Unknown Issue",
            "constitutional_articles": [],
            "case_laws": [],
            "legal_reasoning": "Insufficient articles retrieved to establish legal reasoning.",
            "arguments_for": "N/A",
            "arguments_against": "N/A",
            "possible_verdict": "Relevant constitutional provisions could not be confidently identified.",
            "confidence": "Low"
        }
        return {
            "confidence_score": 0.2,
            "final_answer": "Relevant constitutional provisions could not be confidently identified.",
            "verdict": "Relevant constitutional provisions could not be confidently identified.",
            "verdict_data": verdict_data
        }
        
    primary = articles[0]
    supporting = articles[1:] if len(articles) > 1 else []
    best_case = cases[0] if cases else None
    
    art_num = primary.get("article_number", "")
    art_title = primary.get("title", "")
    
    # Predict verdict
    verdict = f"State or government actions violating the criteria set under Article {art_num} ({art_title}) are likely to be declared unconstitutional."
    
    # Calculate confidence based on similarity score of article and validation
    sim_score = primary.get("similarity_score", 0.8)
    confidence = 0.9 if sim_score > 0.6 and best_case else 0.7
    
    # Format the final markdown report
    md_report = f"# Constitutional Analysis Report\n\n"
    md_report += f"## ⚖️ User Query\n> {state.get('user_query')}\n\n"
    
    md_report += f"## 📖 Primary Constitutional Provision\n"
    clause_str = f" (Clause {primary.get('clause')})" if primary.get("clause") else ""
    md_report += f"- **Article {primary.get('article_number')}: {primary.get('title')}{clause_str}**\n"
    md_report += f"  > {primary.get('content')}\n\n"
    
    if supporting:
        md_report += f"## 🔗 Supporting Constitutional Provisions\n"
        for art in supporting:
            c_str = f" (Clause {art.get('clause')})" if art.get("clause") else ""
            md_report += f"- **Article {art.get('article_number')}: {art.get('title')}{c_str}**\n"
            md_report += f"  > {art.get('content')}\n\n"
        
    if cases:
        md_report += f"## 🏛️ Landmark Case Jurisprudence\n"
        for c in cases:
            md_report += f"- **{c.get('case_name')} ({c.get('citation')})**\n"
            md_report += f"  > *Summary:* {c.get('summary')}\n\n"
            
    md_report += f"## 🧠 Legal Reasoning & Analysis\n{reasoning}\n\n"
    md_report += f"## 🎯 Predicted Constitutional Outcome / Verdict\n**{verdict}**\n\n"
    md_report += f"## 📊 Confidence Level: {'High' if confidence >= 0.8 else 'Medium'} ({confidence * 100:.1f}%)\n"
    
    # Structure verdict_data for local offline mode
    const_articles = []
    for art in articles:
        const_articles.append({
            "name": f"Article {art.get('article_number')}: {art.get('title')}",
            "year": "1950",
            "relevance_explanation": f"Specifies protections and provisions under {art.get('title')}."
        })
        
    case_laws = []
    for c in cases:
        case_laws.append({
            "name": c.get("case_name"),
            "year": str(c.get("year", "N/A")),
            "relevance_explanation": f"Landmark case establishing that: {c.get('summary')}."
        })
        
    verdict_data = {
        "issue": category or "Constitutional Protection",
        "constitutional_articles": const_articles,
        "case_laws": case_laws,
        "legal_reasoning": reasoning,
        "arguments_for": "The state action violates the constitutional rights without proper authorization.",
        "arguments_against": "The state may argue public order, safety, or reasonable restrictions.",
        "possible_verdict": verdict,
        "confidence": "High" if confidence >= 0.8 else ("Medium" if confidence >= 0.5 else "Low")
    }
    
    return {
        "confidence_score": confidence,
        "final_answer": md_report,
        "verdict": verdict,
        "verdict_data": verdict_data
    }

def verdict_agent(state: AgentState) -> Dict[str, Any]:
    """
    Verdict Agent: Formulates the final verdict, confidence score, and compiles the final markdown report.
    """
    logger.info("Running Verdict Agent...")
    
    verdict_data = None
    
    llm = get_llm(temperature=0.2)
    if llm:
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            
            # If off-topic, generate a clean stop verdict
            val_res = state.get("validation_result") or {}
            category = state.get("detected_legal_issue") or state.get("category")
            if val_res.get("action") == "stop" or category == "Non-Legal":
                system_prompt = (
                    "You are a helpful Indian Constitutional Law AI Assistant.\n"
                    "The user query is off-topic or not related to constitutional law.\n"
                    "Respond politely explaining that you specialize in Indian Constitutional Law queries.\n"
                    "Respond ONLY in JSON format:\n"
                    "{\n"
                    "  \"issue\": \"Non-Legal / Off-Topic\",\n"
                    "  \"constitutional_articles\": [],\n"
                    "  \"case_laws\": [],\n"
                    "  \"legal_reasoning\": \"The query is off-topic or not related to constitutional law.\",\n"
                    "  \"arguments_for\": \"N/A\",\n"
                    "  \"arguments_against\": \"N/A\",\n"
                    "  \"possible_verdict\": \"Relevant constitutional provisions could not be confidently identified.\",\n"
                    "  \"confidence\": \"Low\"\n"
                    "}"
                )
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Query: {state['user_query']}")
                ]
                response = llm.invoke(messages)
                content = response.content.strip()
                verdict_data = _parse_json_robust(content)
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
                
                # Load verdict prompt template dynamically
                PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")
                prompt_path = os.path.join(PROMPTS_DIR, "verdict_prompt.txt")
                if os.path.exists(prompt_path):
                    with open(prompt_path, "r", encoding="utf-8") as f:
                        system_prompt_template = f.read()
                else:
                    system_prompt_template = (
                        "You are an expert Constitutional Supreme Court Verdict Agent.\n"
                        "Respond ONLY in JSON format:\n"
                        "{{\n"
                        "  \"issue\": \"Core legal issue\",\n"
                        "  \"constitutional_articles\": [],\n"
                        "  \"case_laws\": [],\n"
                        "  \"legal_reasoning\": \"Detailed reasoning\",\n"
                        "  \"arguments_for\": \"Arguments for user\",\n"
                        "  \"arguments_against\": \"Arguments against user\",\n"
                        "  \"possible_verdict\": \"Clear verdict statement\",\n"
                        "  \"confidence\": \"High, Medium, or Low\"\n"
                        "}}"
                    )
                
                system_prompt = system_prompt_template.replace("{query}", state['user_query'])
                system_prompt = system_prompt.replace("{articles_str}", articles_str)
                system_prompt = system_prompt.replace("{cases_str}", cases_str)
                system_prompt = system_prompt.replace("{reasoning}", reasoning)
                system_prompt = system_prompt.replace("{validation_str}", json.dumps(validation))
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Scenario: {state['user_query']}")
                ]
                
                response = llm.invoke(messages)
                content = response.content.strip()
                verdict_data = _parse_json_robust(content)
                
                # Generate a beautiful Markdown report as final_answer based on verdict_data
                md = f"# Constitutional Analysis Report\n\n"
                md += f"## ⚖️ Core Legal Issue\n{verdict_data.get('issue')}\n\n"
                
                md += f"## 📖 Constitutional Provisions\n"
                for art in verdict_data.get("constitutional_articles") or []:
                    md += f"- **{art.get('name')}** (Year: {art.get('year')})\n"
                    md += f"  > *Relevance:* {art.get('relevance_explanation')}\n\n"
                    
                md += f"## 🏛️ Case Jurisprudence\n"
                for case in verdict_data.get("case_laws") or []:
                    md += f"- **{case.get('name')}** (Year: {case.get('year')})\n"
                    md += f"  > *Relevance:* {case.get('relevance_explanation')}\n\n"
                    
                md += f"## 🧠 Legal Reasoning\n{verdict_data.get('legal_reasoning')}\n\n"
                
                md += f"## ⚖️ Balanced Arguments\n"
                md += f"### Arguments For:\n{verdict_data.get('arguments_for')}\n\n"
                md += f"### Arguments Against:\n{verdict_data.get('arguments_against')}\n\n"
                
                md += f"## 🎯 Predicted Outcome / Verdict\n**{verdict_data.get('possible_verdict')}**\n\n"
                md += f"## 📊 Confidence Level: {verdict_data.get('confidence')}\n"
                
                verdict_data["final_answer"] = md
                logger.info("LLM Verdict and report generated.")
        except Exception as e:
            logger.warning(f"LLM verdict agent failed: {e}. Falling back to local verdict.")
            
    if not verdict_data:
        res = generate_verdict_local(state)
        verdict_data = res["verdict_data"]
        verdict_data["final_answer"] = res["final_answer"]
        logger.info("Local Fallback Verdict and report generated.")
        
    # Intercept guardrail for unknown question handling
    articles = state.get("retrieved_articles") or []
    top_score = articles[0].get("similarity_score", 0.0) if articles else 0.0
    category = state.get("detected_legal_issue") or state.get("category")
    val_res = state.get("validation_result") or {}
    
    is_insufficient = (
        (not articles) or 
        (top_score < 0.4) or 
        (category == "Non-Legal") or 
        (val_res.get("action") == "stop") or
        ("more legal data required" in str(verdict_data.get("possible_verdict", "")).lower()) or
        ("not be confidently identified" in str(verdict_data.get("possible_verdict", "")).lower())
    )
    
    if is_insufficient:
        fallback_data = {
            "issue": category or "Non-Legal",
            "constitutional_articles": [],
            "case_laws": [],
            "legal_reasoning": "Relevant constitutional provisions could not be confidently identified.",
            "arguments_for": "N/A",
            "arguments_against": "N/A",
            "possible_verdict": "Relevant constitutional provisions could not be confidently identified.",
            "confidence": "Low"
        }
        return {
            "confidence_score": 0.2,
            "final_answer": "Relevant constitutional provisions could not be confidently identified.",
            "verdict": "Relevant constitutional provisions could not be confidently identified.",
            "verdict_data": fallback_data
        }
        
    # Calculate confidence_score float
    conf_str = str(verdict_data.get("confidence", "Medium")).lower()
    if "high" in conf_str:
        confidence_val = 0.9
    elif "low" in conf_str:
        confidence_val = 0.2
    else:
        confidence_val = 0.6
        
    return {
        "confidence_score": confidence_val,
        "final_answer": verdict_data.get("final_answer", ""),
        "verdict": verdict_data.get("possible_verdict", ""),
        "verdict_data": verdict_data
    }
