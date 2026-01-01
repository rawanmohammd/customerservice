```
---
title: ZEdny AI Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# ZEdny AI - Customer Service Backend

Backend API for intelligent customer service with email notifications.

## Features
- AI-powered issue classification
- Automatic employee assignment
- Email notifications via Gmail SMTP
- RAG-based knowledge retrieval
It uses FastAPI, SentenceTransformers (Hybrid Search), and Groq LLM.

## Environment Variables Required
- `GROQ_API_KEY`: Your Groq API Key
- `EMBEDDING_MODEL`: `all-MiniLM-L6-v2` (Recommended for free CPU tier)
```
