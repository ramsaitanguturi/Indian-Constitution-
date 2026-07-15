import sys
import os
import argparse

# Add backend directory to sys.path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.agent_service import agent_service
from app.core.logging import setup_logging

setup_logging()

def test_case(name: str, query: str):
    print("\n" + "="*90)
    print(f"TEST CASE: {name}")
    print(f"QUERY: \"{query}\"")
    print("="*90)
    
    try:
        response = agent_service.run_query(query, limit=3)
        
        print("\n--- RETRIEVED CONSTITUTION ARTICLES ---")
        if response.articles:
            for idx, art in enumerate(response.articles, 1):
                print(f"[{idx}] Article {art.article_number}: {art.title} (Clause: {art.clause})")
                print(f"    Similarity Score: {art.similarity_score}")
        else:
            print("No matching articles retrieved.")
            
        print("\n--- RETRIEVED LANDMARK CASE LAWS ---")
        if response.cases:
            for idx, case in enumerate(response.cases, 1):
                print(f"[{idx}] {case.case_name} ({case.citation})")
                print(f"    Similarity Score: {case.similarity_score}")
        else:
            print("No matching cases retrieved.")
            
        print("\n--- AGENT GENERATED REASONING ---")
        print(response.reasoning or "No reasoning generated.")
        
        print("\n--- AGENT PREDICTED VERDICT/OUTCOME ---")
        print(response.verdict or "No verdict predicted.")
        
        print("\n--- VERDICT CONFIDENCE ---")
        print(response.confidence or "N/A")
        
    except Exception as e:
        print(f"Error executing test case: {e}")
        import traceback
        traceback.print_exc()
        
    print("="*90 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Test LangGraph Agentic Constitutional RAG Workflow.")
    parser.add_argument("--query", type=str, help="Specific query to test (optional).")
    args = parser.parse_args()
    
    if args.query:
        test_case("Custom Query", args.query)
        return

    test_cases = [
        {
            "name": "Freedom of Speech",
            "query": "Can the government block my peaceful protest?"
        },
        {
            "name": "Privacy",
            "query": "Can police search my phone without a warrant?"
        },
        {
            "name": "Illegal Arrest",
            "query": "What are my rights if I am arrested without a warrant?"
        },
        {
            "name": "Religious Freedom",
            "query": "Can someone wear religious symbols in public spaces?"
        },
        {
            "name": "Equality",
            "query": "Is arbitrary discrimination by the state illegal?"
        },
        {
            "name": "Off-topic Query (Router Stop Check)",
            "query": "How do I bake a chocolate cake?"
        }
    ]
    
    print("Starting LangGraph Agentic Workflow Verification Test Suite...")
    for tc in test_cases:
        test_case(tc["name"], tc["query"])

if __name__ == "__main__":
    main()
