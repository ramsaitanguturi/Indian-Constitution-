import os
import json
import re
from typing import Dict, Any, List
from app.core.config import settings, get_llm
from app.core.logging import logger

class ConceptService:
    def __init__(self):
        self.concepts = {}
        self.load_concepts()

    def load_concepts(self):
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            concepts_path = os.path.join(backend_dir, "data", "raw", "legal_concepts.json")
            if os.path.exists(concepts_path):
                with open(concepts_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.concepts = {item["concept_name"]: {
                        "articles": item.get("related_articles", []),
                        "cases": item.get("related_cases", []),
                        "keywords": item.get("keywords", []),
                        "legal_explanation": item.get("legal_explanation", "")
                    } for item in data}
                else:
                    self.concepts = data
                logger.info(f"ConceptService loaded {len(self.concepts)} concepts.")
            else:
                logger.warning(f"ConceptService: legal_concepts.json not found at {concepts_path}")
        except Exception as e:
            logger.error(f"ConceptService failed to load legal_concepts.json: {e}")

    def detect_concepts(self, query_text: str) -> Dict[str, Any]:
        """
        Detect legal issue, related articles, cases, and keywords.
        Uses Gemini LLM if API key is available, falls back to keyword-based matching.
        """
        logger.info(f"ConceptService detecting concepts for: '{query_text}'")
        
        llm = get_llm(temperature=0.0)
        if llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage

                concepts_list_str = ", ".join(self.concepts.keys())
                system_prompt = (
                    "You are an expert Indian Constitutional Law legal intelligence assistant.\n"
                    "Analyze the user's query and extract the legal concept details.\n"
                    f"Predefined legal issues/categories: {concepts_list_str}.\n\n"
                    "If the query matches or is closely related to a predefined category, use that category name as 'legal_issue'. "
                    "Determine the relevant constitutional articles (e.g. 'Article 21'), landmark Supreme Court cases (e.g. 'Justice K.S. Puttaswamy v. Union of India'), "
                    "and relevant keywords. If it is completely off-topic, set 'legal_issue' to 'Non-Legal'. If it is legal but doesn't match any predefined category, set 'legal_issue' to 'General Legal Query'.\n\n"
                    "Respond ONLY in valid JSON format:\n"
                    "{\n"
                    "  \"legal_issue\": \"Category Name or General Legal Query or Non-Legal\",\n"
                    "  \"related_articles\": [\"Article X\", \"Article Y\"],\n"
                    "  \"related_cases\": [\"Case A v. Case B\"],\n"
                    "  \"keywords\": [\"keyword1\", \"keyword2\"]\n"
                    "}"
                )

                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Query: {query_text}")
                ]

                response = llm.invoke(messages)
                content = response.content.strip()
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    content = match.group(0)

                result = json.loads(content)
                logger.info(f"ConceptService LLM result: {result}")
                
                # Validation and mapping reinforcement:
                # If LLM identified a predefined category, let's make sure its canonical cases/articles are present
                category = result.get("legal_issue")
                if category in self.concepts:
                    mapped_info = self.concepts[category]
                    # Merge articles
                    for art in mapped_info.get("articles", []):
                        if art not in result["related_articles"]:
                            result["related_articles"].append(art)
                    # Merge cases
                    for case in mapped_info.get("cases", []):
                        if case not in result["related_cases"]:
                            result["related_cases"].append(case)
                            
                return result
            except Exception as e:
                logger.warning(f"ConceptService LLM detection failed: {e}. Falling back to rule-based matching.")

        # Fallback to rule-based keyword matching
        return self._detect_concepts_rule_based(query_text)

    def _detect_concepts_rule_based(self, query_text: str) -> Dict[str, Any]:
        cleaned = query_text.lower().strip()
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        words = cleaned.split()
        
        best_category = None
        best_score = 0
        
        for category, details in self.concepts.items():
            score = 0
            keywords = details.get("keywords", [])
            for kw in keywords:
                kw_clean = kw.lower().strip()
                kw_clean = re.sub(r'[^\w\s]', ' ', kw_clean)
                kw_clean = re.sub(r'\s+', ' ', kw_clean)
                
                if " " in kw_clean:
                    if kw_clean in cleaned:
                        score += 3  # multi-word match gets high weight
                else:
                    if kw_clean in words:
                        score += 2  # exact word match
                    elif any(kw_clean in w for w in words):
                        score += 1  # substring match
            
            if score > best_score:
                best_score = score
                best_category = category
                
        if best_category and best_score >= 2:
            logger.info(f"Rule-based matched category: {best_category} (Score: {best_score})")
            mapped = self.concepts[best_category]
            return {
                "legal_issue": best_category,
                "related_articles": mapped.get("articles", []),
                "related_cases": mapped.get("cases", []),
                "keywords": mapped.get("keywords", [])
            }
            
        # Fallback to general legal query or non-legal
        legal_keywords = ["law", "court", "judge", "right", "constitution", "article", "legal", "government", "state", "police", "arrest", "citizen", "illegal", "unconstitutional", "demolish", "demolition", "religion", "religious", "speech", "equality", "reservation", "president", "parliament", "legislature", "ordinance", "school", "military", "army", "pollution", "environment"]
        if any(kw in cleaned for kw in legal_keywords):
            logger.info("Rule-based fallback: General Legal Query")
            return {
                "legal_issue": "General Legal Query",
                "related_articles": [],
                "related_cases": [],
                "keywords": []
            }
            
        logger.info("Rule-based fallback: Non-Legal")
        return {
            "legal_issue": "Non-Legal",
            "related_articles": [],
            "related_cases": [],
            "keywords": []
        }

concept_service = ConceptService()
