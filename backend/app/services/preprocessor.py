import re
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger

class QueryPreprocessor:
    def __init__(self):
        # Fallback expansion rules for test cases
        self.rules = [
            {
                "keys": ["speech", "expression", "protest", "speak", "voice", "assembly", "gather", "march", "demonstration", "union", "association"],
                "keywords": ["freedom of speech", "expression", "peaceful assembly", "protest", "association"],
                "expansions": ["Article 19", "Article 19(1)(a)", "Article 19(1)(b)", "Article 19(2)", "freedom of speech and expression", "reasonable restrictions", "public order", "Shreya Singhal v. Union of India"]
            },
            {
                "keys": ["privacy", "private", "surveillance", "phone", "device", "search", "warrant", "permission", "wiretap", "tap", "tracking", "spy"],
                "keywords": ["right to privacy", "surveillance", "unwarranted search", "device search"],
                "expansions": ["Article 21", "right to privacy", "personal liberty", "search warrant", "informational privacy", "Justice K.S. Puttaswamy v. Union of India", "proportionality test"]
            },
            {
                "keys": ["arrest", "arrested", "detain", "detained", "custody", "police", "magistrate", "24 hours", "lawyer", "consult", "bail"],
                "keywords": ["arrest", "police custody", "magistrate production", "detention rights"],
                "expansions": ["Article 22", "Article 22(1)", "Article 22(2)", "Article 21", "grounds of arrest", "right to legal counsel", "production before magistrate within 24 hours", "D.K. Basu v. State of West Bengal", "Union of India v. K.A. Najeeb", "speedy trial", "bail"]
            },
            {
                "keys": ["religion", "religious", "faith", "worship", "wear", "symbol", "hijab", "turban", "church", "temple", "mosque", "conscience", "propagate"],
                "keywords": ["freedom of religion", "religious practice", "conscience", "religious symbols"],
                "expansions": ["Article 25", "Article 25(1)", "freedom of conscience", "practice and propagation of religion", "secularism", "Bijoe Emmanuel v. State of Kerala"]
            },
            {
                "keys": ["equality", "equal", "discrimination", "discriminate", "arbitrary", "class", "protection", "laws", "alike"],
                "keywords": ["equality before law", "discrimination", "arbitrariness", "equal protection"],
                "expansions": ["Article 14", "equality before law", "equal protection of the laws", "reasonable classification", "non-arbitrariness", "State of West Bengal v. Anwar Ali Sarkar", "Maneka Gandhi v. Union of India"]
            }
        ]

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
        """
        cleaned = self.clean_query(query_text)
        
        # Attempt LLM preprocess if OpenAI key is present
        if settings.OPENAI_API_KEY:
            try:
                return self._preprocess_llm(query_text, cleaned)
            except Exception as e:
                logger.warning(f"LLM preprocessing failed: {e}. Falling back to local rules.")

        # Local fallback
        keywords = self.extract_keywords_local(cleaned)
        expansions = self.expand_query_local(cleaned)
        
        # Create a combined search string
        search_query = query_text
        if expansions:
            search_query += " " + " ".join(expansions)

        return {
            "cleaned_query": cleaned,
            "keywords": keywords,
            "expansions": expansions,
            "search_query": search_query
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
