# Constitution RAG Backend

This is the backend service for the Constitution RAG Agent, built with FastAPI, LangGraph, and ChromaDB.

## Setup Instructions

### 1. Python Virtual Environment Setup

We recommend using Python 3.10+ (tested on Python 3.12.10).

1. Open a PowerShell/Terminal window in the `backend` directory:
   ```powershell
   cd backend
   ```
2. Create the virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate the virtual environment:
   * **Windows PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows CMD:**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   * **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

### 2. Install Dependencies

Install the required packages:
```powershell
pip install -r requirements.txt
```

### 3. Environment Variables Setup

Create a `.env` file in the `backend` directory:
```env
# Optional: Provide OpenAI key if you want to use OpenAI API for embeddings or LLM reasoning
OPENAI_API_KEY=your_openai_api_key_here

# Embedding provider: "local" (default) or "openai"
EMBEDDING_PROVIDER=local

# Persistent ChromaDB storage path (default is backend/data/chroma)
CHROMADB_DIR=data/chroma
```

## Running the Application

### 1. Seed & Ingest the Constitution Data

Before querying, run the ingestion script to parse, chunk, and embed the dataset into ChromaDB:
```powershell
python scripts/ingest_data.py
```

### 2. Run the Verification Script

Verify that the vector search and parent-child retrieval is working:
```powershell
python scripts/test_rag.py --query "Can government stop a peaceful protest?"
```

### 3. Start the FastAPI Web Server

Run the development server:
```powershell
uvicorn app.main:app --reload
```
Once running, you can access:
* **Interactive API Documentation (Swagger UI):** `http://localhost:8000/docs`
* **Health Check Endpoint:** `http://localhost:8000/health`
* **Search Endpoint:** `POST http://localhost:8000/api/v1/chat/search`

## Memory Optimizations & Model Tuning (Optional)

This backend is optimized for constrained memory environments and resource-limited local systems:

### 1. Memory Optimization Features
- **Lazy Loading**: The heavy `SentenceTransformer` model weights are NOT loaded during server startup or container probes (e.g. `/health`). They are only loaded on the first query request.
- **Singleton Client**: ChromaDB `PersistentClient` is initialized as a thread-safe singleton, preventing SQLite connection duplication and memory inflation across multiple threads.

### 2. Tuning Embedding Models (RAM constraints)
By default, the backend uses `all-MiniLM-L6-v2` (approx. 120MB weights, ~200MB RAM). If your deployment environment still runs into memory limits during query processing:
1. Open your `.env` file or set the system environment variables:
   ```env
   LOCAL_EMBEDDING_MODEL="sentence-transformers/paraphrase-MiniLM-L3-v2"
   ```
2. Re-ingest the data to update the vector embeddings using the new model:
   ```powershell
   python scripts/ingest_data.py
   ```
This lighter model (61MB weights, ~100MB RAM) runs significantly faster and takes about half the memory footprint.

