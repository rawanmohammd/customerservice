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
        # 1. PURGE ALL EMPLOYEES (Clean Slate) - Requested by User
        # This ensures no old data (like Sarah) remains.
        # Note: In a real production app, you wouldn't do this, but for this demo/testing phase it's perfect.
        from sqlmodel import delete
        statement = delete(Employee)
        session.exec(statement)
        session.commit()
        print("🔥 Startup: DELETED ALL EMPLOYEES (Clean Slate) 🧹")
        
        # 2. SEED RAWAN (Test Employee)
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

        # 3. SEED OPERATIONS MANAGER (New Request)
        statement = select(Employee).where(Employee.email == "mohammedraab635@gmail.com")
        ops_existing = session.exec(statement).first()
        
        if not ops_existing:
            print("🚀 Startup: Creating Operations Manager...")
            ops_employee = Employee(
                name="Mohammed (Ops Manager)",
                email="mohammedraab635@gmail.com",
                department="operations",
                role="manager",
                is_active=True
            )
            session.add(ops_employee)
            session.commit()
        else:
            print(f"✅ Startup: Operations Manager {ops_existing.name} already exists.")

@app.get("/version")
def get_version():
    return {
        "version": "1.6.0 (NUCLEAR UPDATE)",
        "last_updated": "2026-01-01 22:20",
        "description": "Forced clean DB & Docker Rebuild"
    }

@app.get("/verify-employees")
def verify_employees():
    """DIRECT endpoint in main.py to verify employees without routing issues."""
    from sqlmodel import Session, select
    from app.core.database import engine
    from app.models.models import Employee
    
    with Session(engine) as session:
        employees = session.exec(select(Employee)).all()
        return employees

# Register Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(debug.router, prefix="/api/debug", tags=["Debug"])

@app.get("/")
def read_root():
    return {"message": "ZEdny AI Backend is Running 🚀"}
