# Vidhi.AI - Local Docker Orchestration Guide (Optional)

This document describes how to build, run, and verify the local containerized stack of the multi-agent Constitution RAG assistant (**Vidhi.AI**) using Docker and Docker Compose.

---

## Prerequisites

Ensure you have the following installed on your host system:
1. **Docker** (v20.10 or higher)
2. **Docker Compose** (v2.0 or higher)

---

## Environment Setup

The backend service requires model credentials to run. Create a `.env` file in the root workspace directory containing:

```ini
# Google API Key for Gemini LLM
GOOGLE_API_KEY=your_google_api_key_here

# Optional: OpenAI API Key if EMBEDDING_PROVIDER is set to "openai"
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Container Setup Steps

### 1. Build and Start Services
To build the local Docker images and start backend and frontend containers, execute:

```bash
docker compose up -d --build
```

This will:
- Build the FastAPI backend image and start it on port `8000`.
- Mount a persistent volume named `vidhi_chroma_data` to store the indexed database.
- Build the React frontend with Vite, compile assets, configure custom Nginx fallbacks, and serve the application on port `80`.

### 2. Verify Running Containers
Check that both containers are running successfully:

```bash
docker compose ps
```

---

## Verifying the Local API

You can verify that the system is fully operational by calling the backend endpoints directly:

### 1. Health Status
Check the status of the server and the live ChromaDB connection:
```bash
curl http://localhost:8000/health
```

### 2. System Information
Check the model setup and indexed document details:
```bash
curl http://localhost:8000/system-info
```

### 3. Legal RAG Query
Submit a test legal scenario directly to the endpoint:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Can the police search my phone without a warrant?", "limit": 3}'
```

---

## Stop Services

To stop and remove containers but keep persistent database volumes:
```bash
docker compose down
```

To stop containers and delete database indexes:
```bash
docker compose down -v
```
