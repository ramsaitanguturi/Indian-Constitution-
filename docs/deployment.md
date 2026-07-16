# Deployment Guide for Vidhi.AI Constitution Legal Assistant

This guide explains how to build, test, and deploy the **Vidhi.AI Constitution Legal Assistant** to production environments.

---

## 1. Local Deployment (Docker Compose)

The easiest way to run the entire stack locally in a production-like containerized environment is using Docker Compose.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A valid **Gemini API Key** (from Google AI Studio).

### Setup and Start
1. Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your `GOOGLE_API_KEY`:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```
3. Build and launch the containers:
   ```bash
   docker compose up -d --build
   ```
4. Verify the applications are running:
   - **Frontend**: Navigate to `http://localhost`
   - **Backend API**: Navigate to `http://localhost:8000/docs` to see the interactive Swagger UI.

---

## 2. Backend Deployment

The Python FastAPI backend is stateless (using ChromaDB on local volume or memory for fast lookups) and can be deployed to any container-based cloud service. We recommend **Render** or **Railway**.

### Option A: Deploying on Render (Web Service)
1. **Create a New Web Service**:
   - Connect your GitHub repository.
   - Choose the `backend` subdirectory as the root directory (`Root Directory: backend`).
   - Select **Docker** as the runtime. Render will automatically detect the `Dockerfile` inside the `backend` directory.
   - Select the Instance Type (e.g., Free or Starter).
2. **Environment Variables**:
   Under **Environment**, add the following variables:
   - `GOOGLE_API_KEY` (Required): Your Google Gemini API Key.
   - `BACKEND_CORS_ORIGINS` (Optional): Set this to `["https://your-frontend-domain.vercel.app"]` to restrict cross-origin requests in production, or `["*"]` to allow all.
   - `EMBEDDING_PROVIDER`: `local` (uses local SentenceTransformers, no OpenAI key required).
   - `GEMINI_MODEL`: `gemini-2.5-flash`
3. **Deploy**:
   - Click **Create Web Service**. Render will build the Docker container and expose a public URL (e.g., `https://vidhi-backend.onrender.com`).

### Option B: Deploying on Railway
1. **Start a New Project**:
   - Choose **Deploy from GitHub repo**.
   - Select the repository and set the root directory to `backend`.
2. **Configure Variables**:
   - Go to the service settings and add `GOOGLE_API_KEY`.
   - Railway automatically exposes the port defined in the Dockerfile (`8000`).
3. **Deploy**:
   - Railway will detect the Dockerfile, run the build, and deploy the service.

---

## 3. Frontend Deployment

The React frontend compiles down to static HTML, CSS, and JS assets. We recommend deploying to **Vercel** for optimal performance, global CDN distribution, and instant rollbacks.

### Deploying on Vercel
1. **Import the Project**:
   - Go to your Vercel Dashboard and click **Add New** > **Project**.
   - Import your GitHub repository.
2. **Configure Project Settings**:
   - **Framework Preset**: `Vite` (automatically detected).
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. **Environment Variables**:
   Add the following environment variable to link the frontend to the deployed backend:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: The public URL of your deployed backend service (e.g., `https://vidhi-backend.onrender.com`).
4. **Deploy**:
   - Click **Deploy**. Vercel will build the frontend assets and provide a production domain.

---

## 4. Production Security Check and Secrets Management

Before launching:
- **Never** commit API keys or real credentials to Git. Ensure they are listed in `.gitignore` and are supplied only via cloud provider secret managers.
- **CORS Configuration**: Restrict the `BACKEND_CORS_ORIGINS` in your backend deployment settings to point strictly to the frontend Vercel URL to avoid unauthorized access from other websites.
- **SSL**: Both Render and Vercel automatically supply SSL certificates. Ensure all API calls from the frontend use `https://` URLs.
