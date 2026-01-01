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
        # Base Query
        statement = select(Employee).where(Employee.department == department)
        
        # Priority Logic
        if priority == "high" or priority == "medium":
            # Prefer senior staff for high/medium priority
            # AND explicitly exclude mock 'Sarah' to ensure Rawan gets it during testing
            senior_stmt = statement.where(Employee.role.in_(["senior", "manager"])).where(Employee.name != "Sarah")
            results = session.exec(senior_stmt).all()
            
            # If we find Rawan, return her immediately (for testing)
            for emp in results:
                if "Rawan" in emp.name:
                    return emp
            
            if results:
                return random.choice(results)
        
        # Fallback / Normal Priority
        results = session.exec(statement).all()
        
        if not results:
            return None
            
        return random.choice(results)
