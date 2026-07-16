import re
import os
import json
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger

class QueryPreprocessor:
    def __init__(self):
        # Load legal concepts mapping
        self.concepts = {}
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
                logger.info(f"Loaded {len(self.concepts)} legal concepts from legal_concepts.json.")
            else:
                logger.warning(f"legal_concepts.json not found at {concepts_path}")
        except Exception as e:
            logger.warning(f"Failed to load legal concepts in QueryPreprocessor: {e}")

        # Fallback expansion rules for test cases
        self.rules = [
            {
                "keys": ["speech", "expression", "protest", "speak", "voice", "assembly", "gather", "march", "demonstration", "union", "association"],
                "keywords": ["freedom of speech", "expression", "peaceful assembly", "protest", "association"],
                "expansions": ["Article 19", "Article 19(1)(a)", "Article 19(1)(b)", "Article 19(2)", "freedom of speech and expression", "reasonable restrictions", "public order", "Shreya Singhal v. Union of India", "Romesh Thappar v. State of Madras"]
            },
            {
                "keys": ["privacy", "private", "surveillance", "phone", "device", "search", "warrant", "permission", "wiretap", "tap", "tracking", "spy", "location history"],
                "keywords": ["right to privacy", "surveillance", "unwarranted search", "device search"],
                "expansions": ["Article 21", "right to privacy", "personal liberty", "search warrant", "informational privacy", "Justice K.S. Puttaswamy v. Union of India", "proportionality test", "Kharak Singh v. State of UP", "Govind v. State of MP", "PUCL v. Union of India"]
            },
            {
                "keys": ["arrest", "arrested", "detain", "detained", "custody", "police", "magistrate", "24 hours", "lawyer", "consult", "bail", "undertrial", "speedy trial", "handcuff"],
                "keywords": ["arrest", "police custody", "magistrate production", "detention rights"],
                "expansions": ["Article 22", "Article 22(1)", "Article 22(2)", "Article 21", "grounds of arrest", "right to legal counsel", "production before magistrate within 24 hours", "D.K. Basu v. State of West Bengal", "Union of India v. K.A. Najeeb", "Arnesh Kumar v. State of Bihar", "speedy trial", "bail", "Prem Shankar Shukla v. Delhi Administration", "Sunil Batra v. Delhi Administration", "Hussainara Khatoon v. State of Bihar"]
            },
            {
                "keys": ["religion", "religious", "faith", "worship", "wear", "symbol", "hijab", "turban", "church", "temple", "mosque", "conscience", "propagate", "talaq", "marriage"],
                "keywords": ["freedom of religion", "religious practice", "conscience", "religious symbols"],
                "expansions": ["Article 25", "Article 25(1)", "Article 26", "freedom of conscience", "practice and propagation of religion", "secularism", "Bijoe Emmanuel v. State of Kerala", "Sabarimala Temple Case", "Shayara Bano v. Union of India"]
            },
            {
                "keys": ["equality", "equal", "discrimination", "discriminate", "arbitrary", "class", "protection", "laws", "alike", "transgender", "third gender", "same-sex", "adultery", "commission", "female"],
                "keywords": ["equality before law", "discrimination", "arbitrariness", "equal protection"],
                "expansions": ["Article 14", "Article 15", "equality before law", "equal protection of the laws", "reasonable classification", "non-arbitrariness", "State of West Bengal v. Anwar Ali Sarkar", "Maneka Gandhi v. Union of India", "E.P. Royappa v. State of Tamil Nadu", "National Legal Services Authority v. Union of India", "Joseph Shine v. Union of India", "Secretary, Ministry of Defence v. Babita Puniya"]
            },
            {
                "keys": ["reservation", "quota", "ews", "creamy layer", "backward class", "public sector job", "100% reservation", "promotions", "seniority"],
                "keywords": ["reservation quota", "creamy layer", "ews quota", "promotions quota"],
                "expansions": ["Article 16", "Article 16(4)", "Article 16(4A)", "Article 15(4)", "Article 15(5)", "Article 15(6)", "Article 16(6)", "Indra Sawhney v. Union of India", "Janhit Abhiyan v. Union of India", "M. Nagaraj v. Union of India", "Jarnail Singh v. Lachhmi Narain Gupta"]
            },
            {
                "keys": ["governor", "dismiss", "dissolve", "assembly", "summon", "ministry", "cabinet", "emergency", "president's rule", "356", "352"],
                "keywords": ["governor's power", "assembly dissolution", "president's rule", "emergency powers"],
                "expansions": ["Article 356", "Article 163", "Article 164", "S.R. Bommai v. Union of India", "Nabam Rebia v. Deputy Speaker", "State of Rajasthan v. Union of India"]
            },
            {
                "keys": ["ordinance", "promulgat", "repromulgat", "legislature", "session"],
                "keywords": ["ordinance power", "repromulgation of ordinance"],
                "expansions": ["Article 123", "Article 213", "D.C. Wadhwa v. State of Bihar", "Krishna Kumar Singh v. State of Bihar"]
            },
            {
                "keys": ["education", "school", "college", "seats", "children", "minority", "autonomy", "capitation"],
                "keywords": ["right to education", "minority institution", "admission autonomy"],
                "expansions": ["Article 21A", "Article 30", "Article 29", "Unni Krishnan v. State of AP", "Mohini Jain v. State of Karnataka", "T.M.A. Pai Foundation v. State of Karnataka", "P.A. Inamdar v. State of Maharashtra"]
            },
            {
                "keys": ["property", "land acquisition", "highway project", "compensation", "take my land", "demolish", "demolition", "bulldozer", "house", "pavement", "slum"],
                "keywords": ["right to property", "deprivation of property", "housing right", "livelihood"],
                "expansions": ["Article 300A", "Article 21", "Olga Tellis v. Bombay Municipal Corp.", "Jilubhai Nanbhai Khachar v. State of Gujarat"]
            },
            {
                "keys": ["environment", "pollution", "toxic", "gas leak", "chemical", "natural resources", "river", "industry", "hazard", "absolute liability", "polluter pays", "public trust"],
                "keywords": ["clean environment", "absolute liability", "polluter pays", "public trust doctrine"],
                "expansions": ["Article 21", "Article 48A", "M.C. Mehta v. Union of India", "Vellore Citizens Welfare Forum v. Union of India", "M.C. Mehta v. Kamal Nath", "Subhash Kumar v. State of Bihar"]
            },
            {
                "keys": ["election", "vote", "voter", "ballot", "constituency", "candidate", "disqualif", "convict", "antecedents", "bcci"],
                "keywords": ["conduct of elections", "disqualification of politicians", "voter information"],
                "expansions": ["Article 19", "Article 102", "Article 191", "Article 324", "Lily Thomas v. Union of India", "Association for Democratic Reforms v. Union of India", "Mohinder Singh Gill v. Chief Election Commissioner", "Kihoto Hollohan v. Zachillhu"]
            }
        ]

    def match_concepts(self, cleaned_query: str) -> Dict[str, Any]:
        matched_names = []
        concept_articles = set()
        concept_cases = set()
        concept_keywords = set()
        
        words = set(cleaned_query.split())
        
        for name, details in self.concepts.items():
            name_lower = name.lower()
            match_found = name_lower in cleaned_query
            if not match_found:
                for kw in details.get("keywords", []):
                    kw_lower = kw.lower()
                    if " " in kw_lower:
                        if kw_lower in cleaned_query:
                            match_found = True
                            break
                    else:
                        if kw_lower in words or any(kw_lower in w for w in words):
                            match_found = True
                            break
            
            if match_found:
                matched_names.append(name)
                for art in details.get("articles", []):
                    concept_articles.add(art)
                for case in details.get("cases", []):
                    concept_cases.add(case)
                for kw in details.get("keywords", []):
                    concept_keywords.add(kw)
                    
        return {
            "matched_concepts": matched_names,
            "concept_articles": list(concept_articles),
            "concept_cases": list(concept_cases),
            "concept_keywords": list(concept_keywords)
        }

    def clean_query(self, query_text: str) -> str:
        """
        Cleans the query by lowercasing, stripping whitespace, and removing special characters.
        """
        cleaned = query_text.lower().strip()
        cleaned = re.sub(r'[^\w\s\?]', '', cleaned)
        return cleaned

    def extract_keywords_local(self, cleaned_query: str) -> List[str]:
        """
        Rule-based keyword extraction.
        """
        extracted = set()
        words = cleaned_query.split()
        for rule in self.rules:
            for key in rule["keys"]:
                if key in words or any(key in w for w in words):
                    for kw in rule["keywords"]:
                        extracted.add(kw)
        
        # Simple noun/stopword filter fallback if nothing extracted
        if not extracted:
            stopwords = {"can", "the", "a", "an", "police", "government", "state", "my", "your", "his", "her", "their", "without", "with", "for", "to", "in", "on", "at", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did"}
            for w in words:
                if len(w) > 3 and w not in stopwords:
                    extracted.add(w)
        
        return list(extracted)

    def expand_query_local(self, cleaned_query: str) -> List[str]:
        """
        Rule-based query expansion.
        """
        expanded = set()
        for rule in self.rules:
            # Check if any key matches
            if any(key in cleaned_query for key in rule["keys"]):
                for exp in rule["expansions"]:
                    expanded.add(exp)
        return list(expanded)

    def preprocess(self, query_text: str) -> Dict[str, Any]:
        """
        Preprocesses a user query.
        Returns:
            - cleaned_query: Cleaned query text
            - keywords: List of extracted legal keywords
            - expansions: List of expanded legal terms
            - search_query: Fully expanded string to use in hybrid retrieval
            - matched_concepts: Matched concept names
            - concept_articles: Mapped article numbers
            - concept_cases: Mapped landmark case names
        """
        cleaned = self.clean_query(query_text)
        
        # Concept matching
        concept_info = self.match_concepts(cleaned)
        
        # Local fallback
        keywords = self.extract_keywords_local(cleaned)
        expansions = self.expand_query_local(cleaned)
        
        # Merge concept info
        for kw in concept_info["concept_keywords"]:
            if kw not in keywords:
                keywords.append(kw)
                
        expansions_set = set(expansions)
        for art in concept_info["concept_articles"]:
            expansions_set.add(art)
        for case in concept_info["concept_cases"]:
            expansions_set.add(case)
        expansions = list(expansions_set)
        
        # Create a combined search string
        search_query = query_text
        if expansions:
            search_query += " " + " ".join(expansions)

        return {
            "cleaned_query": cleaned,
            "keywords": keywords,
            "expansions": expansions,
            "search_query": search_query,
            "matched_concepts": concept_info["matched_concepts"],
            "concept_articles": concept_info["concept_articles"],
            "concept_cases": concept_info["concept_cases"]
        }

    def _preprocess_llm(self, query_text: str, cleaned_query: str) -> Dict[str, Any]:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        prompt = f"""You are a constitutional law AI preprocessor.
Analyze the following legal query:
"{query_text}"

Perform:
1. Legal Keyword Extraction: Extract 2-4 core legal keywords/concepts.
2. Query Expansion: Add relevant constitutional terms, articles, or landmark cases that are likely involved.

Respond ONLY in JSON format:
{{
  "keywords": ["keyword1", "keyword2"],
  "expansions": ["expansion1", "expansion2"]
}}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a legal assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        import json
        data = json.loads(response.choices[0].message.content)
        keywords = data.get("keywords", [])
        expansions = data.get("expansions", [])
        
        search_query = query_text
        if expansions:
            search_query += " " + " ".join(expansions)
            
        return {
            "cleaned_query": cleaned_query,
            "keywords": keywords,
            "expansions": expansions,
            "search_query": search_query
        }

query_preprocessor = QueryPreprocessor()
