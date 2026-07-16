# Local Execution & Orchestration Guide for Vidhi.AI Constitution Legal Assistant

This guide explains how to run, configure, and orchestrate the **Vidhi.AI Constitution Legal Assistant** locally on your machine. This project is configured to run exclusively in local environments.

---

## 1. Native Bare-Metal Local Setup (Recommended)

To run the application natively on your local system:

### Prerequisites
- Python 3.10+ (tested on Python 3.12.10)
- Node.js (v18 or higher) and npm
- A valid **Gemini API Key** (from Google AI Studio)

### A. Backend FastAPI Server
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables in `backend/.env`:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   EMBEDDING_PROVIDER=local
   LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
   BACKEND_CORS_ORIGINS=["*"]
   ```
5. Seed/ingest the Constitution and case law data into the local ChromaDB:
   ```bash
   python scripts/ingest_data.py
   ```
6. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will be live on `http://localhost:8000`. Access the interactive Swagger API documentation at `http://localhost:8000/docs`.

### B. Frontend React App
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure the local environment variables in `frontend/.env`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```
4. Start the frontend developer server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## 2. Local Containerized Orchestration (Optional)

Alternatively, you can run the entire stack locally in containerized environments using Docker and Docker Compose.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Setup and Start
1. Create a `.env` file in the root workspace directory:
   ```bash
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```
2. Build and launch the containers:
   ```bash
   docker compose up -d --build
   ```
3. Verify the applications:
   - **Frontend React Web App**: Access `http://localhost`
   - **Backend FastAPI Service**: Access Swagger docs at `http://localhost:8000/docs`
4. Tear down the containers:
   ```bash
   docker compose down -v
   ```
