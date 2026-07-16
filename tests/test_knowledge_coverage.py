import sys
import os

# Add backend directory to sys.path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(workspace_root, "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.agent_service import agent_service
from app.core.logging import setup_logging

setup_logging()

TEST_CASES = [
    # 1. Freedom of speech & internet
    {
        "query": "Can government block internet?",
        "expected_article": "19",
        "expected_case": "Anuradha Bhasin",
        "is_legal": True
    },
    {
        "query": "Can the government block my peaceful protest?",
        "expected_article": "19",
        "expected_case": "Shreya Singhal",
        "is_legal": True
    },
    {
        "query": "Does freedom of the press allow newspapers to publish without pre-censorship?",
        "expected_article": "19",
        "expected_case": "Romesh Thappar",
        "is_legal": True
    },
    
    # 2. Privacy
    {
        "query": "Can police search my phone without a warrant?",
        "expected_article": "21",
        "expected_case": "Puttaswamy",
        "is_legal": True
    },
    {
        "query": "The police tapped my phone and started wiretapping my conversations without a warrant. Is this legal?",
        "expected_article": "21",
        "expected_case": "Puttaswamy",
        "is_legal": True
    },
    {
        "query": "Can the police conduct night-time surveillance and domiciliary visits at my house without permission?",
        "expected_article": "21",
        "expected_case": "Kharak Singh",
        "is_legal": True
    },
    
    # 3. Arrest & Detention
    {
        "query": "Can police arrest without informing reason?",
        "expected_article": "22",
        "expected_case": "D.K. Basu",
        "is_legal": True
    },
    {
        "query": "I was arrested by the police last night and kept in custody for 30 hours without being produced before a magistrate.",
        "expected_article": "22",
        "expected_case": "D.K. Basu",
        "is_legal": True
    },
    {
        "query": "What are my rights if I am arrested without a warrant?",
        "expected_article": "22",
        "expected_case": "D.K. Basu",
        "is_legal": True
    },
    {
        "query": "Can the police handcuff an accused person during transit to court?",
        "expected_article": "21",
        "expected_case": "Prem Shankar Shukla",
        "is_legal": True
    },
    {
        "query": "What are the safeguards against preventive detention order?",
        "expected_article": "22",
        "expected_case": "A.K. Gopalan",
        "is_legal": True
    },
    
    # 4. Property Rights
    {
        "query": "Can government acquire private property?",
        "expected_article": "300A",
        "expected_case": "Jilubhai",
        "is_legal": True
    },
    {
        "query": "The municipal corporation brought bulldozers and demolished my house without giving any prior legal notice.",
        "expected_article": "300A",
        "expected_case": "Olga Tellis",
        "is_legal": True
    },
    
    # 5. Religious Freedom
    {
        "query": "Can religious practice be restricted?",
        "expected_article": "25",
        "expected_case": "Sabarimala",
        "is_legal": True
    },
    {
        "query": "Can the state expel children from school for refusing to sing the National Anthem due to religious beliefs?",
        "expected_article": "25",
        "expected_case": "Bijoe Emmanuel",
        "is_legal": True
    },
    {
        "query": "Can someone wear religious symbols in public spaces?",
        "expected_article": "25",
        "expected_case": "Bijoe Emmanuel",
        "is_legal": True
    },
    {
        "query": "Can a religious denomination manage its own property without state interference?",
        "expected_article": "26",
        "expected_case": "Sabarimala",
        "is_legal": True
    },
    
    # 6. Reservation & Equality
    {
        "query": "Can reservation exceed 50 percent?",
        "expected_article": "16",
        "expected_case": "Indra Sawhney",
        "is_legal": True
    },
    {
        "query": "Can the government implement a 10% quota for economically weaker sections in public employment?",
        "expected_article": "16",
        "expected_case": "Janhit Abhiyan",
        "is_legal": True
    },
    {
        "query": "Can the state implement SC/ST reservation in promotions?",
        "expected_article": "16",
        "expected_case": "M. Nagaraj",
        "is_legal": True
    },
    {
        "query": "Does the creamy layer exclusion rule apply to SC/ST promotions quotas?",
        "expected_article": "16",
        "expected_case": "Jarnail Singh",
        "is_legal": True
    },
    {
        "query": "Is arbitrary discrimination by the state illegal?",
        "expected_article": "14",
        "expected_case": "Anwar Ali Sarkar",
        "is_legal": True
    },
    {
        "query": "Does equality before law mean identical treatment or reasonable classification?",
        "expected_article": "14",
        "expected_case": "Anwar Ali Sarkar",
        "is_legal": True
    },
    
    # 7. Governor & Executive
    {
        "query": "Can governor dismiss state government?",
        "expected_article": "164",
        "expected_case": "S.R. Bommai",
        "is_legal": True
    },
    {
        "query": "The President declared President's Rule in our state and dissolved the assembly. Is this valid?",
        "expected_article": "356",
        "expected_case": "S.R. Bommai",
        "is_legal": True
    },
    {
        "query": "Does the Governor have absolute discretionary power to summon or dissolve the state assembly?",
        "expected_article": "163",
        "expected_case": "Nabam Rebia",
        "is_legal": True
    },
    {
        "query": "Can the President issue ordinances when Parliament is not in session?",
        "expected_article": "123",
        "expected_case": "D.C. Wadhwa",
        "is_legal": True
    },
    {
        "query": "Is re-promulgation of ordinances without placing them before the legislature valid?",
        "expected_article": "213",
        "expected_case": "D.C. Wadhwa",
        "is_legal": True
    },
    
    # 8. Education & Minority Rights
    {
        "query": "Do minority institutions have autonomy to run their schools without reservation quotas?",
        "expected_article": "30",
        "expected_case": "P.A. Inamdar",
        "is_legal": True
    },
    {
        "query": "Is the right to education a fundamental right for children under 14?",
        "expected_article": "21A",
        "expected_case": "Unni Krishnan",
        "is_legal": True
    },
    {
        "query": "Can private schools charge arbitrary capitation fees for admission?",
        "expected_article": "21A",
        "expected_case": "Mohini Jain",
        "is_legal": True
    },
    
    # 9. Civil Rights & Gender
    {
        "query": "Are female military officers entitled to permanent commission in the army?",
        "expected_article": "14",
        "expected_case": "Babita Puniya",
        "is_legal": True
    },
    {
        "query": "Is instant triple talaq unconstitutional and discriminatory against women?",
        "expected_article": "14",
        "expected_case": "Shayara Bano",
        "is_legal": True
    },
    {
        "query": "Is consensual gay sex between adults a criminal offense under the constitution?",
        "expected_article": "21",
        "expected_case": "Navtej Singh Johar",
        "is_legal": True
    },
    {
        "query": "Does the right to life protect a person's sexual orientation and partner choice?",
        "expected_article": "21",
        "expected_case": "Shafin Jahan",
        "is_legal": True
    },
    {
        "query": "Are transgender people recognized as a third gender with fundamental rights?",
        "expected_article": "21",
        "expected_case": "National Legal Services Authority",
        "is_legal": True
    },
    {
        "query": "Is the criminal adultery law unconstitutional as it treats women as property?",
        "expected_article": "14",
        "expected_case": "Joseph Shine",
        "is_legal": True
    },
    
    # 10. Environmental Law
    {
        "query": "Is the state responsible for protecting natural resources under the Public Trust Doctrine?",
        "expected_article": "21",
        "expected_case": "Kamal Nath",
        "is_legal": True
    },
    {
        "query": "Does the right to clean environment include protection against industrial toxic gas leaks?",
        "expected_article": "21",
        "expected_case": "M.C. Mehta",
        "is_legal": True
    },
    {
        "query": "Must a polluting industry pay for ecological restoration under the Polluter Pays principle?",
        "expected_article": "21",
        "expected_case": "Vellore Citizens",
        "is_legal": True
    },
    {
        "query": "Is absolute liability applicable to enterprises engaged in hazardous activities?",
        "expected_article": "21",
        "expected_case": "M.C. Mehta",
        "is_legal": True
    },
    
    # 11. Constitutional Structure & Writs
    {
        "query": "Can the parliament amend the basic structure of the constitution under Article 368?",
        "expected_article": "368",
        "expected_case": "Kesavananda",
        "is_legal": True
    },
    {
        "query": "Are laws in the Ninth Schedule immune from judicial review post 1973?",
        "expected_article": "31B",
        "expected_case": "I.R. Coelho",
        "is_legal": True
    },
    {
        "query": "Can writ jurisdiction of High Courts under Article 226 be excluded by administrative tribunals?",
        "expected_article": "226",
        "expected_case": "L. Chandra Kumar",
        "is_legal": True
    },
    {
        "query": "Can a public-spirited citizen file a PIL on behalf of marginalized workers?",
        "expected_article": "32",
        "expected_case": "S.P. Gupta",
        "is_legal": True
    },
    {
        "query": "Can an accused challenge forced narco-analysis testing as self-incrimination?",
        "expected_article": "20",
        "expected_case": "Selvi",
        "is_legal": True
    },
    
    # 12. Elections & Disqualification
    {
        "query": "Do convicted politicians lose their seats immediately upon conviction?",
        "expected_article": "102",
        "expected_case": "Lily Thomas",
        "is_legal": True
    },
    {
        "query": "Does a voter have the right to know the criminal antecedents and assets of candidates?",
        "expected_article": "19",
        "expected_case": "Association for Democratic Reforms",
        "is_legal": True
    },
    
    # 13. Unknown/Off-topic cases
    {
        "query": "How do I bake a chocolate cake?",
        "expected_article": "None",
        "expected_case": "None",
        "is_legal": False
    },
    {
        "query": "What is the best way to write a React front-end page?",
        "expected_article": "None",
        "expected_case": "None",
        "is_legal": False
    },
    {
        "query": "Explain the rules of cricket and the role of the BCCI.",
        "expected_article": "None",
        "expected_case": "None",
        "is_legal": False
    }
]

def run_coverage_benchmark():
    print("=" * 120)
    print("                EVALUATING PHASE 5B: LEGAL KNOWLEDGE COVERAGE BENCHMARK (50 TESTS)")
    print("=" * 120)
    
    passed_count = 0
    total_count = len(TEST_CASES)
    
    for idx, tc in enumerate(TEST_CASES, 1):
        query = tc["query"]
        expected_art = tc["expected_article"]
        expected_case = tc["expected_case"]
        is_legal = tc["is_legal"]
        
        print(f"\n[{idx}/{total_count}] Query: \"{query}\"")
        
        try:
            response = agent_service.run_query(query, limit=3)
            
            # Check articles and cases retrieved
            retrieved_arts = [a.article_number for a in response.articles]
            retrieved_cases = [c.case_name for c in response.cases]
            verdict = response.verdict
            confidence = response.confidence
            
            print(f"      Retrieved Articles : {retrieved_arts}")
            print(f"      Retrieved Cases    : {retrieved_cases}")
            print(f"      Confidence         : {confidence}")
            print(f"      Verdict            : {verdict[:100]}...")
            
            # Match validation
            art_matched = False
            case_matched = False
            unknown_correct = False
            
            if is_legal:
                art_matched = any(expected_art in a for a in retrieved_arts)
                case_matched = any(expected_case.lower() in c.lower() for c in retrieved_cases)
                test_passed = art_matched and case_matched
            else:
                unknown_correct = (
                    verdict == "Relevant constitutional provisions could not be confidently identified." and
                    not response.articles
                )
                test_passed = unknown_correct
                
            if test_passed:
                print(f"      --> TEST RESULT: PASS")
                passed_count += 1
            else:
                reason = []
                if is_legal:
                    if not art_matched: reason.append(f"Missing expected Article {expected_art}")
                    if not case_matched: reason.append(f"Missing expected Case '{expected_case}'")
                else:
                    if not unknown_correct: reason.append("Failed to detect unknown/off-topic query correctly")
                print(f"      --> TEST RESULT: FAIL ({', '.join(reason)})")
                
        except Exception as e:
            print(f"      --> TEST ERROR: {e}")
            
        print("-" * 120)
        
    print(f"\nFinal Benchmark Summary: {passed_count}/{total_count} scenarios passed successfully.")
    print(f"Knowledge Coverage Accuracy: {(passed_count/total_count)*100:.2f}%")
    print("=" * 120 + "\n")

if __name__ == "__main__":
    run_coverage_benchmark()
