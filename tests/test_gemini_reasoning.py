import sys
import os
import json

# Add backend directory to sys.path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(workspace_root, "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.core.config import settings
from app.services.agent_service import agent_service
from app.core.logging import setup_logging

setup_logging()

TEST_QUERIES = {
    "privacy": "The police tapped my phone and started wiretapping my conversations without a warrant. Is this legal?",
    "arrest": "I was arrested by the police last night and kept in custody for 30 hours without being produced before a magistrate.",
    "property demolition": "The municipal corporation brought bulldozers and demolished my house without giving any prior legal notice or time to vacate.",
    "reservation": "Can the government implement a 10% quota for economically weaker sections in public employment and admission?",
    "emergency powers": "The President has declared President's Rule in our state and dissolved the legislative assembly. Is this constitutionally valid?"
}

def format_response_comparison(category: str, before_res, after_res):
    print("=" * 120)
    print(f" CATEGORY: {category.upper()}")
    print(f" Query: {TEST_QUERIES[category]}")
    print("=" * 120)
    
    # Print Before Gemini Upgrade (Fallback)
    print("\n[BEFORE GEMINI REASONING (LOCAL RULE-BASED FALLBACK)]")
    print(f"  - Issue             : {before_res.issue}")
    print(f"  - Possible Verdict  : {before_res.possible_verdict}")
    print(f"  - Confidence Level  : {before_res.confidence}")
    print(f"  - Legal Reasoning   : {before_res.legal_reasoning}")
    print(f"  - Arguments For     : {before_res.arguments_for}")
    print(f"  - Arguments Against : {before_res.arguments_against}")
    print(f"  - Articles Cited    : {[art.name for art in before_res.constitutional_articles]}")
    print(f"  - Cases Cited       : {[case.name for case in before_res.case_laws]}")
    
    # Print After Gemini Upgrade
    print("\n[AFTER GEMINI REASONING (GOOGLE GEMINI API INTEGRATION)]")
    print(f"  - Issue             : {after_res.issue}")
    print(f"  - Possible Verdict  : {after_res.possible_verdict}")
    print(f"  - Confidence Level  : {after_res.confidence}")
    print(f"  - Legal Reasoning   : {after_res.legal_reasoning}")
    print(f"  - Arguments For     : {after_res.arguments_for}")
    print(f"  - Arguments Against : {after_res.arguments_against}")
    print(f"  - Articles Cited    : {[{'name': art.name, 'year': art.year, 'relevance': art.relevance_explanation} for art in after_res.constitutional_articles]}")
    print(f"  - Cases Cited       : {[{'name': case.name, 'year': case.year, 'relevance': case.relevance_explanation} for case in after_res.case_laws]}")
    print("-" * 120)

def main():
    original_api_key = settings.GOOGLE_API_KEY
    
    # Double check if GOOGLE_API_KEY is available in env if not in settings
    if not original_api_key:
        original_api_key = os.environ.get("GOOGLE_API_KEY")
        settings.GOOGLE_API_KEY = original_api_key
        
    if not original_api_key:
        print("WARNING: GOOGLE_API_KEY environment variable is not set. Gemini API requests will fail and both runs will fall back to local offline mode.")
        print("Please export GOOGLE_API_KEY before running the tests to see the actual LLM output comparison.")
        
    comparison_data = {}
    
    for key, query in TEST_QUERIES.items():
        print(f"Evaluating scenario '{key}'...")
        
        # 1. Run "Before Gemini" - Disable GOOGLE_API_KEY to force local fallback
        settings.GOOGLE_API_KEY = None
        before_response = agent_service.run_query(query, limit=3)
        
        # 2. Run "After Gemini" - Restore GOOGLE_API_KEY
        settings.GOOGLE_API_KEY = original_api_key
        after_response = agent_service.run_query(query, limit=3)
        
        comparison_data[key] = {
            "before": before_response,
            "after": after_response
        }
        
    for key in TEST_QUERIES.keys():
        format_response_comparison(key, comparison_data[key]["before"], comparison_data[key]["after"])

if __name__ == "__main__":
    main()
