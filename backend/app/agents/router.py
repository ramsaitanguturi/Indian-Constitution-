import json
import re
from typing import Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.services.preprocessor import query_preprocessor
from app.agents.state import AgentState

def classify_query_local(query_text: str) -> Dict[str, Any]:
    """
    Fallback deterministic classification for local/offline mode.
    """
    cleaned = query_text.lower()
    
    # 1. Check for specific categories
    if any(k in cleaned for k in ["speech", "expression", "protest", "speak", "voice", "assembly", "gather", "march", "demonstration"]):
        return {
            "category": "Freedom of Speech",
            "issue": "Restrictions on peaceful expression or assembly",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["arrest", "arrested", "detain", "detained", "custody", "magistrate"]):
        return {
            "category": "Illegal Arrest",
            "issue": "Procedural safeguards against arbitrary arrest or detention",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["privacy", "private", "surveillance", "phone", "device", "search", "warrant", "permission", "wiretap", "tap"]):
        return {
            "category": "Privacy",
            "issue": "Unwarranted device search, surveillance, or privacy intrusion",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["religion", "religious", "faith", "worship", "wear", "symbol", "hijab", "turban"]):
        return {
            "category": "Religious Freedom",
            "issue": "State interference in freedom of conscience and religious practice",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["equality", "equal", "discrimination", "discriminate", "arbitrary", "class", "protection"]):
        return {
            "category": "Equality",
            "issue": "Violation of right to equality and equal protection under arbitrary state action",
            "action": "proceed"
        }
    
    # 2. General legal queries
    legal_keywords = ["law", "court", "judge", "right", "constitution", "article", "legal", "government", "state", "police", "arrest", "citizen", "illegal", "unconstitutional", "verdict"]
    if any(kw in cleaned for kw in legal_keywords):
        return {
            "category": "General Legal Query",
            "issue": "General constitutional query or legal scenario",
            "action": "proceed"
        }
        
    # 3. Off-topic queries
    return {
        "category": "Non-Legal",
        "issue": "Off-topic query not related to Indian constitutional law",
        "action": "stop"
    }

def router_agent(state: AgentState) -> Dict[str, Any]:
    """
    Router Agent: Classifies query intent and extracts the legal issue.
    """
    logger.info("Running Router Agent...")
    query = state["user_query"]
    
    # 1. Run RAG query preprocessing
    processed = query_preprocessor.preprocess(query)
    
    classification = None
    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import SystemMessage, HumanMessage
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2
            )
            
            system_prompt = (
                "You are an expert Indian Constitutional Law routing assistant.\n"
                "Analyze the user's legal scenario and classify it into one of these categories:\n"
                "- Freedom of Speech\n"
                "- Privacy\n"
                "- Illegal Arrest\n"
                "- Religious Freedom\n"
                "- Equality\n"
                "- General Legal Query\n"
                "- Non-Legal\n\n"
                "Decide if the query is a valid legal/constitutional query (action='proceed') or completely "
                "unrelated to law/constitution (action='stop').\n\n"
                "Respond ONLY in valid JSON format:\n"
                "{\n"
                "  \"category\": \"Category Name\",\n"
                "  \"issue\": \"Concise description of the detected legal issue\",\n"
                "  \"action\": \"proceed\" or \"stop\"\n"
                "}"
            )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Query: {query}")
            ]
            
            response = llm.invoke(messages)
            
            # Simple regex to extract JSON if LLM returned markdown wrapped JSON
            content = response.content.strip()
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                content = match.group(0)
            
            classification = json.loads(content)
            logger.info(f"LLM Classification: {classification}")
        except Exception as e:
            logger.warning(f"LLM router failed: {e}. Falling back to rule-based router.")
            
    if not classification:
        classification = classify_query_local(query)
        logger.info(f"Local Fallback Classification: {classification}")
        
    return {
        "processed_query": processed,
        "detected_legal_issue": classification.get("category", "General Legal Query"),
        "validation_result": {
            "action": classification.get("action", "proceed"),
            "category": classification.get("category", "General Legal Query"),
            "issue": classification.get("issue", "")
        }
    }
