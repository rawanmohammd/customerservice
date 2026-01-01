from sqlmodel import Session, select
from app.models.models import Employee, Issue
import random

class AssignmentService:
    @staticmethod
    def assign_employee(session: Session, department: str, priority: str) -> Employee | None:
        """
        Finds the best employee for the job.
        Rule 1: Filter by Department
        Rule 2: If High Priority -> Look for 'Senior' or 'Manager' role
        Rule 3: Randomly pick one to simulate load balancing (Round Robin ideal in prod)
        """
        
        # Base Query
        statement = select(Employee).where(Employee.department == department)
        
        # Priority Logic
        if priority == "high":
            # Prefer senior staff for high priority
            senior_stmt = statement.where(Employee.role.in_(["senior", "manager"]))
            results = session.exec(senior_stmt).all()
            if results:
                return random.choice(results)
        
        # Fallback / Normal Priority
        results = session.exec(statement).all()
        
        if not results:
            return None
            
        return random.choice(results)
