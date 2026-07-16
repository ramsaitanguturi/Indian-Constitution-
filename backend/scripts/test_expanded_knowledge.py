import sys
import os

# Add backend directory to sys.path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.agent_service import agent_service
from app.core.logging import setup_logging

setup_logging()

test_cases = [
    {
        "category": "Privacy",
        "query": "Can the police trace my location history without a warrant?",
        "expected_primary_article": "21",
        "expected_case": "Justice K.S. Puttaswamy"
    },
    {
        "category": "Arrest",
        "query": "What happens if police arrest me and don't take me to a judge for two days?",
        "expected_primary_article": "22",
        "expected_case": "D.K. Basu"
    },
    {
        "category": "Freedom of Speech",
        "query": "Can the government ban my blog post criticizing a state policy?",
        "expected_primary_article": "19",
        "expected_case": "Shreya Singhal"
    },
    {
        "category": "Religious Freedom",
        "query": "Can the state forbid a student from wearing a turban in a classroom?",
        "expected_primary_article": "25",
        "expected_case": "Bijoe Emmanuel"
    },
    {
        "category": "Reservation",
        "query": "Can a public sector job have 100% reservation for a specific community?",
        "expected_primary_article": "16",
        "expected_case": "Indra Sawhney"
    },
    {
        "category": "Elections",
        "query": "Can a state official alter voter lists without oversight?",
        "expected_primary_article": "324",
        "expected_case": "Mohinder Singh Gill"
    },
    {
        "category": "Emergency Powers",
        "query": "Can the President dissolve a state assembly arbitrarily?",
        "expected_primary_article": "356",
        "expected_case": "S.R. Bommai"
    },
    {
        "category": "Federal Disputes",
        "query": "Can two states sue each other over river water sharing in the Supreme Court?",
        "expected_primary_article": "262", # or 131
        "expected_case": "State of Karnataka"
    },
    {
        "category": "Property Rights",
        "query": "Can the government take my land for a highway project without paying any compensation?",
        "expected_primary_article": "300A",
        "expected_case": "Jilubhai Nanbhai Khachar"
    },
    {
        "category": "Education Rights",
        "query": "Is a private school required to provide free seats to underprivileged children?",
        "expected_primary_article": "21A",
        "expected_case": "Unni Krishnan"
    },
    {
        "category": "Missing Knowledge (Low Confidence)",
        "query": "What is the legal punishment for a simple breach of contract under the Indian Contract Act?",
        "expected_primary_article": "None",
        "expected_low_confidence": True
    }
]

def run_test_suite():
    print("=" * 110)
    print("                    INDIAN CONSTITUTION RAG KNOWLEDGE EXPANSION TEST SUITE")
    print("=" * 110)
    
    passed_articles = 0
    passed_cases = 0
    passed_confidence = 0
    total_tests = len(test_cases)
    
    for idx, tc in enumerate(test_cases, 1):
        print(f"\n[{idx}/{total_tests}] Category: {tc['category']}")
        print(f"Query: \"{tc['query']}\"")
        print("-" * 50)
        
        try:
            response = agent_service.run_query(tc["query"], limit=3)
            
            # 1. Verify Article Retrieval
            retrieved_nums = [art.article_number for art in response.articles]
            primary_ok = False
            if tc["expected_primary_article"] == "None":
                # Expect no highly relevant articles or no articles at all
                primary_ok = (len(response.articles) == 0 or response.articles[0].similarity_score < 0.35)
            else:
                primary_ok = (len(response.articles) > 0 and response.articles[0].article_number == tc["expected_primary_article"])
                
            if primary_ok:
                print("[PASS] Primary Article Match: PASSED")
                passed_articles += 1
            else:
                print(f"[FAIL] Primary Article Match: FAILED (Expected: {tc['expected_primary_article']}, Got: {retrieved_nums[0] if retrieved_nums else 'None'})")
                
            # 2. Verify Case Retrieval
            case_ok = False
            retrieved_cases = [c.case_name for c in response.cases]
            if tc["expected_primary_article"] == "None":
                case_ok = True  # N/A
                passed_cases += 1
            else:
                # Check substring match of expected case in any of the top 3 retrieved cases
                for c in retrieved_cases:
                    if tc["expected_case"].lower() in c.lower():
                        case_ok = True
                        break
                if case_ok:
                    print("[PASS] Case Law Match: PASSED")
                    passed_cases += 1
                else:
                    print(f"[FAIL] Case Law Match: FAILED (Expected containing: '{tc['expected_case']}', Got: {retrieved_cases})")
                    
            # 3. Verify Confidence & Verdict Warning
            confidence_ok = False
            if tc.get("expected_low_confidence"):
                confidence_ok = (response.confidence == "Low" and "More legal data required for a stronger answer." in response.verdict)
                if confidence_ok:
                    print("[PASS] Low Confidence Detection: PASSED")
                    passed_confidence += 1
                else:
                    print(f"[FAIL] Low Confidence Detection: FAILED (Got confidence: {response.confidence}, verdict: {response.verdict})")
            else:
                confidence_ok = (response.confidence in ["High", "Medium"])
                if confidence_ok:
                    print("[PASS] Confidence Match: PASSED")
                    passed_confidence += 1
                else:
                    print(f"[FAIL] Confidence Match: FAILED (Expected High/Medium, Got: {response.confidence})")
                    
            print(f"Primary Provision: Article {response.articles[0].article_number if response.articles else 'N/A'} - {response.articles[0].title if response.articles else 'N/A'}")
            if len(response.articles) > 1:
                print(f"Supporting Provisions: {', '.join(['Article ' + a.article_number for a in response.articles[1:]])}")
            print(f"Retrieved Case: {response.cases[0].case_name if response.cases else 'N/A'}")
            print(f"Verdict Outcome: {response.verdict[:100]}...")
            
        except Exception as e:
            print(f"[ERROR] Test execution encountered error: {e}")
            import traceback
            traceback.print_exc()
            
        print("-" * 50)
        
    print("\n" + "=" * 110)
    print("                                     SUMMARY RESULTS")
    print("=" * 110)
    print(f"Article Retrieval Accuracy: {passed_articles}/{total_tests} ({passed_articles/total_tests*100:.1f}%)")
    print(f"Case Retrieval Accuracy: {passed_cases - 1 if 'expected_low_confidence' in test_cases[-1] else passed_cases}/{total_tests - 1} ({(passed_cases - 1)/(total_tests - 1)*100:.1f}%)")
    print(f"Confidence & Warning Accuracy: {passed_confidence}/{total_tests} ({passed_confidence/total_tests*100:.1f}%)")
    print("=" * 110)

if __name__ == "__main__":
    run_test_suite()
