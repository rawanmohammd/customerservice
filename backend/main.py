from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.api import chat, issues, debug

app = FastAPI(title="ZEdny AI Backend", version="1.0.0")

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    # In production, specific domains are safer, but for this demo deployment '*' allows Vercel connectivity easier.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(debug.router, prefix="/api/debug", tags=["Debug"])

@app.get("/")
def read_root():
    return {"message": "ZEdny AI Backend is Running 🚀"}
