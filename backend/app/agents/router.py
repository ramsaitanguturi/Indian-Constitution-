import json
import re
from typing import Dict, Any
from app.core.config import settings, get_llm
from app.core.logging import logger
from app.services.preprocessor import query_preprocessor
from app.agents.state import AgentState

def classify_query_local(query_text: str) -> Dict[str, Any]:
    """
    Fallback deterministic classification for local/offline mode.
    """
    cleaned = query_text.lower().strip()
    
    # 1. Check for specific categories first to avoid general shadow matches
    # Emergency Powers must be checked before Freedom of Speech due to 'assembly' keyword overlap
    if any(k in cleaned for k in ["emergency", "president's rule", "356", "352", "dissolve", "state assembly", "dissolve a state assembly", "national emergency", "president rule", "ordinance", "ordinances", "promulgation", "re-promulgation"]):
        return {
            "category": "Emergency Powers",
            "issue": "Exercise of emergency powers and imposition of President's Rule",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["speech", "expression", "protest", "speak", "voice", "peaceful assembly", "right to assemble", "gather", "march", "demonstration", "blog", "criticiz", "press", "censor", "newspaper", "internet", "shutdown", "block"]):
        return {
            "category": "Freedom of Speech",
            "issue": "Restrictions on peaceful expression or assembly",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["education", "school", "seats", "children", "compulsory education", "free seats"]):
        return {
            "category": "Education Rights",
            "issue": "Right to education and regulation of private schools",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["property", "land acquisition", "highway project", "compensation", "take my land", "demolish", "demolition"]):
        return {
            "category": "Property Rights",
            "issue": "Deprivation of property and entitlement to compensation",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["federal dispute", "river water", "inter-state water", "center-state", "two states sue"]):
        return {
            "category": "Federal Disputes",
            "issue": "Adjudication of water disputes and center-state jurisdictional conflicts",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["election", "vote", "voter", "ballot", "constituency", "alter voter", "electoral"]):
        return {
            "category": "Elections",
            "issue": "Powers of the Election Commission and conduct of elections",
            "action": "proceed"
        }
    # For Reservation, check 'ews', 'sc', 'st', 'obc' with word boundaries
    reservation_keywords = ["reservation", "quota", "creamy layer", "backward class", "public sector job", "100% reservation"]
    has_reservation = any(k in cleaned for k in reservation_keywords) or any(re.search(r'\b' + k + r'\b', cleaned) for k in ["ews", "sc", "st", "obc"])
    if has_reservation:
        return {
            "category": "Reservation",
            "issue": "Constitutional limits and safeguards on caste/economic reservations",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["religion", "religious", "faith", "worship", "wear", "symbol", "hijab", "turban", "sabarimala", "denomination"]):
        return {
            "category": "Religious Freedom",
            "issue": "State interference in freedom of conscience and religious practice",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["arrest", "arrested", "detain", "detained", "custody", "magistrate", "judge for two days", "grounds of arrest", "handcuff", "self-incrim", "incrimin", "jeopardy", "ex-post facto", "detention", "preventive"]):
        return {
            "category": "Illegal Arrest",
            "issue": "Procedural safeguards against arbitrary arrest or detention",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["privacy", "surveillance", "phone tapping", "device search", "search without warrant", "wiretap", "tap", "tracking", "spy", "location history", "trace my location", "environment", "pollution", "pollut", "gas leak", "liability", "toxic", "hazardous", "ecological", "restoration"]):
        return {
            "category": "Privacy",
            "issue": "Unwarranted device search, surveillance, or privacy intrusion",
            "action": "proceed"
        }
    if any(k in cleaned for k in ["equality", "equal", "discrimination", "discriminate", "arbitrary", "class", "protection", "transgender", "third gender", "same-sex", "adultery", "talaq", "military", "army", "commission", "female"]):
        return {
            "category": "Equality",
            "issue": "Violation of right to equality and equal protection under arbitrary state action",
            "action": "proceed"
        }
    
    # 2. General legal queries
    legal_keywords = ["law", "court", "judge", "right", "constitution", "article", "legal", "government", "state", "police", "citizen", "illegal", "unconstitutional", "verdict", "religion", "religious", "speech", "equality", "reservation", "president", "parliament", "legislature", "ordinance", "school", "military", "army", "pollution", "environment"]
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

from app.services.concept_service import concept_service

def router_agent(state: AgentState) -> Dict[str, Any]:
    """
    Router Agent: Classifies query intent and extracts the legal issue.
    """
    logger.info("Running Router Agent...")
    query = state["user_query"]
    
    # 1. Run Concept Extraction
    concepts = concept_service.detect_concepts(query)
    
    # 2. Run RAG query preprocessing
    processed = query_preprocessor.preprocess(query)
    
    # 3. Merge concept results into processed query to boost retrieval signals
    processed["concept_info"] = concepts
    if concepts.get("related_articles"):
        processed["concept_articles"] = list(set(processed.get("concept_articles", []) + concepts["related_articles"]))
    if concepts.get("related_cases"):
        processed["concept_cases"] = list(set(processed.get("concept_cases", []) + concepts["related_cases"]))
    if concepts.get("keywords"):
        processed["keywords"] = list(set(processed.get("keywords", []) + concepts["keywords"]))
        # Inject keywords to the search query if they are not already there
        for kw in concepts["keywords"]:
            if kw.lower() not in processed["search_query"].lower():
                processed["search_query"] += " " + kw
                
    # 4. Determine classification from concepts
    concept_to_router = {
        "Privacy": "Privacy",
        "Illegal arrest": "Illegal Arrest",
        "Arrest": "Illegal Arrest",
        "Reservation": "Reservation",
        "Elections": "Elections",
        "Emergency": "Emergency Powers",
        "Emergency powers": "Emergency Powers",
        "Illegal demolition": "Property Rights",
        "Property": "Property Rights",
        "Freedom of speech": "Freedom of Speech",
        "Freedom of the Press": "Freedom of Speech",
        "Press Freedom": "Freedom of Speech",
        "Religion": "Religious Freedom",
        "Equality": "Equality",
        "Federal disputes": "Federal Disputes",
        "Education": "Education Rights",
        "Constitutional remedies": "General Legal Query",
        "Right against Self-Incrimination": "Illegal Arrest",
        "Self-incrimination": "Illegal Arrest",
        "Double Jeopardy": "Illegal Arrest",
        "Ex-post facto": "Illegal Arrest",
        "Speedy trial": "Illegal Arrest",
        "Custodial violence": "Illegal Arrest",
        "Bail": "Illegal Arrest",
        "Transgender rights": "Equality",
        "Gender equality": "Equality",
        "Triple Talaq": "Equality",
        "Adultery": "Equality",
        "Same-sex marriage": "Equality",
        "Public Trust Doctrine": "Privacy",
        "Absolute liability": "Privacy",
        "Polluter Pays": "Privacy",
        "Environmental protection": "Privacy",
        "Clean environment": "Privacy",
    }
    
    local_cls = classify_query_local(query)
    
    classification = None
    if local_cls["category"] not in ["General Legal Query", "Non-Legal"]:
        classification = local_cls
    else:
        concept_issue = concepts.get("legal_issue")
        mapped_category = concept_to_router.get(concept_issue)
        if mapped_category:
            action = "stop" if mapped_category == "Non-Legal" else "proceed"
            classification = {
                "category": mapped_category,
                "issue": f"Scenario relating to {concept_issue}",
                "action": action
            }
        elif concept_issue == "Non-Legal":
            classification = {
                "category": "Non-Legal",
                "issue": "Off-topic query not related to Indian constitutional law",
                "action": "stop"
            }
        
    if not classification:
        llm = get_llm(temperature=0.2)
        if llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage
                
                system_prompt = (
                    "You are an expert Indian Constitutional Law routing assistant.\n"
                    "Analyze the user's legal scenario and classify it into one of these categories:\n"
                    "- Freedom of Speech\n"
                    "- Privacy\n"
                    "- Illegal Arrest\n"
                    "- Religious Freedom\n"
                    "- Equality\n"
                    "- Reservation\n"
                    "- Elections\n"
                    "- Emergency Powers\n"
                    "- Federal Disputes\n"
                    "- Property Rights\n"
                    "- Education Rights\n"
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
        "detected_concepts": concepts,
        "validation_result": {
            "action": classification.get("action", "proceed"),
            "category": classification.get("category", "General Legal Query"),
            "issue": classification.get("issue", "")
        }
    }
