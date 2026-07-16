import sys
import os

# Add backend directory to sys.path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(workspace_root, "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.concept_service import concept_service
from app.services.agent_service import agent_service
from app.core.logging import setup_logging

setup_logging()

TEST_SCENARIOS = [
    {
        "name": "Phone Surveillance",
        "query": "The police tapped my phone and started wiretapping my conversations without a warrant. Is this legal?",
        "expected_issue": "Privacy",
        "expected_article": "21",
        "expected_case": "Puttaswamy"
    },
    {
        "name": "Illegal Demolition",
        "query": "The municipal corporation brought bulldozers and demolished my house without giving any prior legal notice or time to vacate.",
        "expected_issue": "Illegal demolition",
        "expected_article": "300A",
        "expected_case": "Olga Tellis"
    },
    {
        "name": "Reservation",
        "query": "Can the government implement a 10% quota for economically weaker sections in public employment and admission?",
        "expected_issue": "Reservation",
        "expected_article": "16",
        "expected_case": "Indra Sawhney"
    },
    {
        "name": "Arrest Safeguards",
        "query": "I was arrested by the police last night and kept in custody for 30 hours without being produced before a magistrate.",
        "expected_issue": "Illegal arrest",
        "expected_article": "22",
        "expected_case": "D.K. Basu"
    },
    {
        "name": "Election Dispute",
        "query": "The Election Commission has stopped voting in my constituency due to allegations of booth capturing. Can I challenge this decision in court?",
        "expected_issue": "Elections",
        "expected_article": "324",
        "expected_case": "Mohinder Singh Gill"
    },
    {
        "name": "Emergency Powers",
        "query": "The President has declared President's Rule in our state and dissolved the legislative assembly. Is this constitutionally valid?",
        "expected_issue": "Emergency",
        "expected_article": "356",
        "expected_case": "S.R. Bommai"
    }
]

def run_tests():
    print("=" * 120)
    print("                     EVALUATING PHASE 5A: LEGAL INTELLIGENCE LAYER")
    print("=" * 120)
    
    passed_count = 0
    
    for tc in TEST_SCENARIOS:
        print(f"\n>>> TEST SCENARIO: {tc['name']}")
        print(f"    Query: \"{tc['query']}\"")
        print("-" * 120)
        
        # 1. Test Concept Detection
        concepts = concept_service.detect_concepts(tc["query"])
        print(f"    [Concept Service Output]")
        print(f"      Detected Issue : {concepts.get('legal_issue')}")
        print(f"      Mapped Articles: {concepts.get('related_articles')}")
        print(f"      Mapped Cases   : {concepts.get('related_cases')}")
        print(f"      Keywords       : {concepts.get('keywords')}")
        
        # Verify concept service mapping matching
        issue_matched = tc["expected_issue"].lower() in concepts.get("legal_issue", "").lower()
        art_matched = any(tc["expected_article"] in a for a in concepts.get("related_articles", []))
        case_matched = any(tc["expected_case"].lower() in c.lower() for c in concepts.get("related_cases", []))
        
        # 2. Test Agentic Retrieval & Output
        try:
            response = agent_service.run_query(tc["query"], limit=3)
            
            print(f"\n    [RAG Retrieval Results]")
            
            # Print retrieved articles
            retrieved_arts = [f"Article {a.article_number} (Score: {a.similarity_score:.4f})" for a in response.articles]
            print(f"      Retrieved Articles : {', '.join(retrieved_arts) if retrieved_arts else 'None'}")
            
            # Print retrieved cases
            retrieved_cases = [f"{c.case_name} (Score: {c.similarity_score:.4f})" for c in response.cases]
            print(f"      Retrieved Cases    : {', '.join(retrieved_cases) if retrieved_cases else 'None'}")
            
            # Verify if expected article and case were actually retrieved first/high score
            rag_art_matched = any(tc["expected_article"] in a.article_number for a in response.articles)
            rag_case_matched = any(tc["expected_case"].lower() in c.case_name.lower() for c in response.cases)
            
            print(f"\n    [Status Checks]")
            print(f"      Concept Detection Success : {'PASS' if (issue_matched and art_matched and case_matched) else 'FAIL'}")
            print(f"      RAG Article Retrieval Success: {'PASS' if rag_art_matched else 'FAIL'}")
            print(f"      RAG Case Retrieval Success   : {'PASS' if rag_case_matched else 'FAIL'}")
            
            if issue_matched and rag_art_matched and rag_case_matched:
                print(f"      --> TEST RESULT: SUCCESS")
                passed_count += 1
            else:
                print(f"      --> TEST RESULT: FAILED")
                
            print(f"\n    [Predicted Verdict Preview]")
            print(f"      Confidence: {response.confidence}")
            if response.verdict:
                verdict_preview = response.verdict[:150] + "..." if len(response.verdict) > 150 else response.verdict
                print(f"      Verdict   : {verdict_preview}")
            else:
                print("      Verdict   : None")
                
        except Exception as e:
            print(f"    Error running agent query: {e}")
            import traceback
            traceback.print_exc()
            
        print("=" * 120)
        
    print(f"\nTest Summary: {passed_count}/{len(TEST_SCENARIOS)} scenarios passed successfully.")
    print("=" * 120 + "\n")

if __name__ == "__main__":
    run_tests()
