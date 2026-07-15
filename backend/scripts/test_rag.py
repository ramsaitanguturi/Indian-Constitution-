import sys
import os
import argparse

# Add backend directory to sys.path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.rag_service import rag_service
from app.core.logging import setup_logging, logger

# Quiet down unnecessary logs for this output script
setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Test local Constitution RAG database search.")
    parser.add_argument("--query", type=str, required=True, help="The query or legal scenario to search.")
    parser.add_argument("--limit", type=int, default=3, help="Max results to retrieve.")
    args = parser.parse_args()

    response = rag_service.query(args.query, limit=args.limit)

    print("\n" + "="*80)
    print(f"USER QUERY: {response.question}")
    print("="*80)
    
    print("\n=== RETRIEVED CONSTITUTION ARTICLES (CHILD-FIRST RETRIEVED, PARENT EXPANDED) ===")
    if response.articles:
        for idx, art in enumerate(response.articles, 1):
            print(f"\n[{idx}] Article {art.article_number}: {art.title}")
            print(f"    Clause Matched: {art.clause or 'N/A'}")
            print("    Original Content:")
            # Wrap content lines nicely
            content_lines = art.content.split("\n")
            for line in content_lines:
                print(f"      {line}")
    else:
        print("No matching articles retrieved.")

    print("\n=== RETRIEVED LANDMARK CASE LAWS ===")
    if response.cases:
        for idx, case in enumerate(response.cases, 1):
            print(f"\n[{idx}] {case.case_name} ({case.citation})")
            print("    Summary:")
            summary_lines = case.summary.split("\n")
            for line in summary_lines:
                print(f"      {line}")
    else:
        print("No matching cases retrieved.")

    print("\n=== MVP GENERATED REASONING ===")
    print(response.reasoning or "No reasoning generated.")

    print("\n=== MVP PREDICTED OUTCOME/VERDICT ===")
    print(response.verdict or "No verdict predicted.")

    print("\n=== VERDICT CONFIDENCE ===")
    print(response.confidence or "N/A")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
