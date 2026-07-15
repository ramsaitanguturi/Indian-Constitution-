# Constitution RAG Agent

An AI-powered Constitutional Law assistant using:

- Hierarchical Parent-Child RAG
- Agentic RAG
- Vector Search
- LLM Reasoning
- Legal Knowledge Retrieval


## Problem

Finding constitutional articles and understanding possible legal outcomes requires searching hundreds of pages of constitutional documents and court judgments.

This project builds an AI assistant that maps real-world problems to:

1. Constitutional Articles
2. Fundamental Rights
3. Relevant Clauses
4. Court Judgments
5. Possible Verdict


## Example

Input:

"Can my phone be searched without permission?"


Output:

Article:
Article 21 - Right to Privacy


Cases:
Justice K.S. Puttaswamy v Union of India


Possible Verdict:
Unreasonable search violates privacy rights.


## Features

- Parent Child RAG
- Multi-agent reasoning
- Article retrieval
- Case law retrieval
- Verdict prediction
- Explainable answers


## Architecture

User
 |
Frontend
 |
Backend API
 |
Agent Controller
 |
Retriever
 |
Vector Database
 |
LLM
 |
Final Response


## Tech Stack

Frontend:
- React
- Tailwind CSS

Backend:
- FastAPI
- Python

AI:
- LangChain
- LlamaIndex
- Google Gemini / Local fallback

Database:
- ChromaDB / FAISS

Deployment:
- Vercel
- Render