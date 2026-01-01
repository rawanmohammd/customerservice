---
title: Zedny Customer Service AI
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ZEdny AI Backend

This is the backend API for the ZEdny Customer Service AI.
It uses FastAPI, SentenceTransformers (Hybrid Search), and Groq LLM.

## Environment Variables Required
- `GROQ_API_KEY`: Your Groq API Key
- `EMBEDDING_MODEL`: `all-MiniLM-L6-v2` (Recommended for free CPU tier)
