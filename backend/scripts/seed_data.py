import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlmodel import Session, select
from backend.app.core.database import engine, create_db_and_tables
from backend.app.models.models import Employee, Client

def seed_db():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if already seeded
        if session.exec(select(Employee)).first():
            print("Database already seeded.")
            return

        print("Seeding Employees...")
        employees = [
            Employee(name="Ahmed Tech", email="ahmed@zedny.com", department="web", role="senior"),
            Employee(name="Sarah AI", email="sarah@zedny.com", department="ai", role="manager"),
            Employee(name="Mona Content", email="mona@zedny.com", department="content", role="junior"),
            Employee(name="Ali Sales", email="ali@zedny.com", department="sales", role="senior"),
        ]
        session.add_all(employees)
        
        print("Seeding Clients...")
        clients = [
            Client(name="MegaCorp Industries", email="contact@megacorp.com", phone="+123456789"),
            Client(name="Startup Hub", email="ceo@startuphub.io", phone="+987654321"),
            Client(name="Dr. Tarek Clinic", email="info@tarekclinic.com", phone="+201000000"),
        ]
        session.add_all(clients)
        
        session.commit()
        print("✅ Employees & Clients Seeded!")

if __name__ == "__main__":
    from sqlmodel import select
    seed_db()
