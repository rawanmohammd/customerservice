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
    
    # Auto-create Test Employee (Rawan) on startup to ensure she exists on Hugging Face
    from sqlmodel import Session, select
    from app.core.database import engine
    from app.models.models import Employee
    
    with Session(engine) as session:
        # Check if Rawan exists
        statement = select(Employee).where(Employee.email == "mohammedrawan653@gmail.com")
        existing = session.exec(statement).first()
        
        if not existing:
            print("🚀 Startup: Creating Test Employee (Rawan)...")
            test_employee = Employee(
                name="Rawan (Test Lead)",
                email="mohammedrawan653@gmail.com",
                department="ai",
                role="senior",
                is_active=True
            )
            session.add(test_employee)
            session.commit()
        else:
            print(f"✅ Startup: Test Employee {existing.name} already exists.")

@app.get("/version")
def get_version():
    return {
        "version": "1.5.0",
        "last_updated": "2026-01-01 20:55",
        "features": ["Email for ALL priorities", "Exclude Sarah fix", "Auto-seed Rawan"]
    }

# Register Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(debug.router, prefix="/api/debug", tags=["Debug"])

@app.get("/")
def read_root():
    return {"message": "ZEdny AI Backend is Running 🚀"}
