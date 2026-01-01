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
- AI-powered issue classification (Groq LLM)
- Automatic employee assignment
- Email notifications via Gmail SMTP
- RAG-based knowledge retrieval
- Hybrid search with SentenceTransformers

## Tech Stack
- **FastAPI** - Web framework
- **SQLModel** - Database ORM
- **Groq** - LLM for classification
- **SentenceTransformers** - Embeddings
- **Gmail SMTP** - Email service

## Environment Variables
Required secrets in Hugging Face Spaces:
- `GROQ_API_KEY` - Your Groq API key
- `SMTP_EMAIL` - Gmail address for sending
- `SMTP_PASSWORD` - Gmail App Password
