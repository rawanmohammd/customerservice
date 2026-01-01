"""
Quick script to add a test employee to the database.
"""
from sqlmodel import Session, create_engine, select
from app.models.models import Employee
from app.core.database import DATABASE_URL

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)

with Session(engine) as session:
    # Check if test employee exists
    statement = select(Employee).where(Employee.email == "mohammedrawan653@gmail.com")
    existing = session.exec(statement).first()
    
    if existing:
        print(f"✅ Test employee already exists: {existing.name} ({existing.email})")
    else:
        # Create new test employee
        test_employee = Employee(
            name="Test Employee (Rawan)",
            email="mohammedrawan653@gmail.com",
            department="ai",  # Will receive AI-related escalations
            role="senior",
            is_active=True
        )
        session.add(test_employee)
        session.commit()
        session.refresh(test_employee)
        print(f"✅ Created test employee: {test_employee.name} (ID: {test_employee.id})")
        print(f"   Email: {test_employee.email}")
        print(f"   Department: {test_employee.department}")
