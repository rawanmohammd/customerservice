from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.core.database import get_session
from app.models.models import Issue, Employee

router = APIRouter()

@router.get("/", response_model=List[Issue])
def get_issues(session: Session = Depends(get_session)):
    """
    Get all issues for the dashboard.
    """
    issues = session.exec(select(Issue)).all()
    return issues

@router.get("/my-tasks/{employee_id}")
def get_employee_tasks(employee_id: int, session: Session = Depends(get_session)):
    """
    Get issues assigned to a specific employee.
    """
    statement = select(Issue).where(Issue.assigned_to == employee_id)
    return session.exec(statement).all()
