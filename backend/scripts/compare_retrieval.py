import sys
import os
import argparse
import re

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.db.chroma import db_manager
from app.services.rag_service import rag_service
from app.core.logging import setup_logging

setup_logging()

def run_basic_search(query_text: str, limit: int = 3):
    """
    Simulates the basic Phase 1 retrieval:
    - Pure vector search on children collection with raw query.
    - Fetch parent articles.
    - Pure vector search on cases collection.
    """
    children_col = db_manager.get_children_collection()
    parents_col = db_manager.get_parents_collection()
    cases_col = db_manager.get_cases_collection()
    
    # 1. Basic vector search on children
    child_results = children_col.query(
        query_texts=[query_text],
        n_results=limit
    )
    
    retrieved_articles = []
    parent_ids_to_clauses = {}
    if child_results and child_results["ids"] and len(child_results["ids"][0]) > 0:
        matched_metadatas = child_results["metadatas"][0]
        # Basic mapping to parents
        for meta in matched_metadatas:
            p_id = meta.get("parent_id")
            clause_label = meta.get("clause") or f"Article {meta.get('article_number')}"
            if p_id:
                if p_id not in parent_ids_to_clauses:
                    parent_ids_to_clauses[p_id] = []
                parent_ids_to_clauses[p_id].append(clause_label)
                
        if parent_ids_to_clauses:
            parents_data = parents_col.get(ids=list(parent_ids_to_clauses.keys()))
            if parents_data and "ids" in parents_data:
                for i, p_id in enumerate(parents_data["ids"]):
                    meta = parents_data["metadatas"][i]
                    retrieved_articles.append({
                        "article_number": meta.get("article_number"),
                        "title": meta.get("title"),
                        "clauses": parent_ids_to_clauses[p_id]
                    })
                    
    # 2. Basic vector search on cases
    case_results = cases_col.query(
        query_texts=[query_text],
        n_results=limit
    )
    
    retrieved_cases = []
    if case_results and case_results["ids"] and len(case_results["ids"][0]) > 0:
        for i in range(len(case_results["ids"][0])):
            meta = case_results["metadatas"][0][i]
            retrieved_cases.append({
                "case_name": meta.get("case_name"),
                "citation": meta.get("citation")
            })
            
    return {
        "articles": retrieved_articles,
        "cases": retrieved_cases
    }

def print_separator():
    print("-" * 105)

def main():
    test_cases = [
        {"name": "Freedom of Speech", "query": "Can the government block my peaceful protest?"},
        {"name": "Privacy", "query": "Can police search my phone without a warrant?"},
        {"name": "Arrest without Warrant", "query": "What are my rights if I am arrested without a warrant?"},
        {"name": "Religious Freedom", "query": "Can someone wear religious symbols in public spaces?"},
        {"name": "Equality before Law", "query": "Is arbitrary discrimination by the state illegal?"}
    ]
    
    print("=" * 105)
    print("                     CONSTITUTION RAG RETRIEVAL COMPARISON: PHASE 1 vs PHASE 2")
    print("=" * 105)
    
    for tc in test_cases:
        name = tc["name"]
        query = tc["query"]
        
        print(f"\n>>> TEST CASE: {name}")
        print(f"    QUERY: \"{query}\"")
        print_separator()
        
        # Run Basic Phase 1 Search
        basic_res = run_basic_search(query, limit=3)
        
        # Run Advanced Phase 2 Search
        advanced_res = rag_service.query(query, limit=3)
        
        # Print side-by-side comparison of results
        print(f"{'PHASE 1 (BASIC RETRIEVAL)':<50} | {'PHASE 2 (ADVANCED HYBRID + RERANKED)':<50}")
        print_separator()
        
        # Format Articles
        basic_arts = [f"Article {a['article_number']} ({', '.join(a['clauses'])})" for a in basic_res["articles"]]
        adv_arts = [f"Article {a.article_number} (Clause {a.clause}) [Score: {a.similarity_score:.4f}]" for a in advanced_res.articles]
        
        # Format Cases
        basic_cs = [f"{c['case_name']} ({c['citation']})" for c in basic_res["cases"]]
        adv_cs = [f"{c.case_name} ({c.citation}) [Score: {c.similarity_score:.4f}]" for c in advanced_res.cases]
        
        max_art_lines = max(len(basic_arts), len(adv_arts), 1)
        max_case_lines = max(len(basic_cs), len(adv_cs), 1)
        
        print("  Constitutional Provisions:")
        for i in range(max_art_lines):
            b_art = basic_arts[i][:46] + "..." if i < len(basic_arts) and len(basic_arts[i]) > 48 else (basic_arts[i] if i < len(basic_arts) else "")
            a_art = adv_arts[i][:46] + "..." if i < len(adv_arts) and len(adv_arts[i]) > 48 else (adv_arts[i] if i < len(adv_arts) else "")
            print(f"    - {b_art:<46} |     - {a_art:<46}")
            
        print("\n  Landmark Case Laws:")
        for i in range(max_case_lines):
            b_case = basic_cs[i][:46] + "..." if i < len(basic_cs) and len(basic_cs[i]) > 48 else (basic_cs[i] if i < len(basic_cs) else "")
            a_case = adv_cs[i][:46] + "..." if i < len(adv_cs) and len(adv_cs[i]) > 48 else (adv_cs[i] if i < len(adv_cs) else "")
            print(f"    - {b_case:<46} |     - {a_case:<46}")
            
        # Print advanced details
        print("\n  [Phase 2 Preprocessing Details]:")
        preproc = advanced_res.question # we can just run preprocess to show
        from app.services.preprocessor import query_preprocessor
        details = query_preprocessor.preprocess(query)
        print(f"    - Cleaned Query: \"{details['cleaned_query']}\"")
        print(f"    - Keywords     : {details['keywords']}")
        print(f"    - Expansions   : {details['expansions']}")
        print(f"  [Phase 2 Reasoning]: {advanced_res.reasoning}")
        print(f"  [Phase 2 Verdict  ]: {advanced_res.verdict} (Confidence: {advanced_res.confidence})")
        print_separator()

if __name__ == "__main__":
    main()
