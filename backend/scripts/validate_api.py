import urllib.request
import json
import time
import sys

URL = "http://127.0.0.1:8000/api/v1/chat/query"

queries = [
    "Can the government restrict peaceful protests?",
    "Can police search my phone without permission?",
    "What are my rights if arrested without a warrant?"
]

def check_server_health():
    health_url = "http://127.0.0.1:8000/health"
    print("Checking backend server health...")
    for i in range(10):
        try:
            with urllib.request.urlopen(health_url, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"Health Check Success: {data}")
                    return True
        except Exception as e:
            print(f"Waiting for server... ({e})")
            time.sleep(2)
    return False

def test_query(query):
    print("\n" + "="*80)
    print(f"TESTING QUERY: {query}")
    print("="*80)
    
    payload = json.dumps({"query": query, "limit": 3}).encode('utf-8')
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=30) as response:
            duration = time.time() - start_time
            if response.status == 200:
                res_data = json.loads(response.read().decode('utf-8'))
                print(f"Response received in {duration:.2f} seconds.")
                print(json.dumps(res_data, indent=2))
                
                # Validation checks
                required_fields = ["articles", "cases", "reasoning", "validation_result", "verdict", "confidence"]
                missing = [f for f in required_fields if f not in res_data]
                
                if missing:
                    print(f"\n[FAILED] Missing fields: {missing}")
                else:
                    print("\n[SUCCESS] All required fields are present!")
                    
                # Inspect fields
                print(f"- Articles Count: {len(res_data.get('articles', []))}")
                print(f"- Cases Count: {len(res_data.get('cases', []))}")
                print(f"- Reasoning Present: {bool(res_data.get('reasoning'))}")
                print(f"- Validation Result Present: {bool(res_data.get('validation_result'))}")
                print(f"- Verdict Present: {bool(res_data.get('verdict'))}")
                print(f"- Confidence: {res_data.get('confidence')}")
                
            else:
                print(f"[HTTP ERROR] Status: {response.status}")
    except Exception as e:
        print(f"[ERROR] Error testing query: {e}")

if __name__ == "__main__":
    if not check_server_health():
        print("Server not available. Exiting.")
        sys.exit(1)
        
    for q in queries:
        test_query(q)
