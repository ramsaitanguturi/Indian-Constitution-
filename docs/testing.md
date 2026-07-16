# ConstituAI - Testing & Validation Framework

This document outlines the testing, benchmarking, and validation suites for the ConstituAI Constitution Legal Assistant. It covers backend intelligence tests, LLM reasoning evaluations, coverage benchmarks, and frontend verification.

---

## 1. Backend Testing Layer

The backend uses Python's core testing libraries to assert retrieval accuracy and LLM synthesis. All test scripts are placed in the `tests/` directory at the project root.

### A. Legal Intelligence & Concept Mapping Test
* **File:** [test_legal_intelligence.py](file:///c:/Users/ramsa/Desktop/Indian%20Constitution/tests/test_legal_intelligence.py)
* **Purpose:** Asserts that the concept classification service (`ConceptService`) correctly parses a user query, flags key legal concepts, maps the relevant articles, and pulls matching case names before running the multi-agent graph.
* **To Run:**
  ```bash
  python tests/test_legal_intelligence.py
  ```

### B. Gemini Reasoning Upgrade Evaluation
* **File:** [test_gemini_reasoning.py](file:///c:/Users/ramsa/Desktop/Indian%20Constitution/tests/test_gemini_reasoning.py)
* **Purpose:** Compares the output of the multi-agent system when running with Gemini LLM augmentation versus the local rule-based fallback mode. Helpful for analyzing reasoning quality improvement and response structural differences.
* **To Run:**
  ```bash
  # Ensure GOOGLE_API_KEY is configured in your terminal or .env first
  python tests/test_gemini_reasoning.py
  ```

### C. Knowledge Coverage & Accuracy Benchmark (50 Cases)
* **File:** [test_knowledge_coverage.py](file:///c:/Users/ramsa/Desktop/Indian%20Constitution/tests/test_knowledge_coverage.py)
* **Purpose:** The core benchmark suite containing **50 curated legal scenarios** across 13 domains (Privacy, Arrest, Property, Reservation, Religion, Speech, Elections, Emergency, Governor Executive powers, Education/Minority rights, Civil Rights, Environmental Law, and Off-topic/Non-legal tests). It verifies:
  1. The system correctly identifies target constitutional articles.
  2. The system locates expected landmark precedents.
  3. The system gracefully rejects non-legal/off-topic questions (avoiding hallucinations).
* **Metrics Tracked:** Knowledge Retrieval Accuracy (%).
* **To Run:**
  ```bash
  python tests/test_knowledge_coverage.py
  ```

---

## 2. API Manual Validation (Swagger)

FastAPI automatically documents and generates interactive UI for testing all routes.

1. Start the backend locally:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. Navigate to `http://localhost:8000/docs` in your browser.
3. Test endpoints:
   * `GET /health`: Inspect ChromaDB active connection count and server health status.
   * `GET /system-info`: Check loaded LLM parameters and embedding model configuration.
   * `POST /api/v1/chat/query`: Submit custom legal scenarios and view the structured JSON response timeline.

---

## 3. Frontend Build & Asset Verification

The React frontend utilizes Vite for development and compilation.

### A. Run Linting Checks
To verify JS formatting and clean code properties, run `oxlint` (a lightning-fast linter installed in the devDependencies):
```bash
cd frontend
npm run lint
```

### B. Production Compilation Test
Before deploying the code, compile and build assets to verify React and Tailwind CSS bundle integrity:
```bash
cd frontend
npm run build
```
This produces optimized HTML/JS/CSS assets inside the `dist/` directory, ready to be served via the production Nginx proxy.
