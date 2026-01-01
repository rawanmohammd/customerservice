from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.core.database import get_session
from app.models.models import Issue, Employee

router = APIRouter()

@router.get("/recent", response_model=List[dict])
def get_recent_issues_with_details(session: Session = Depends(get_session)):
    """
    Get recent issues WITH employee assignment details for debugging.
    """
    statement = select(Issue).order_by(Issue.id.desc()).limit(10)
    issues = session.exec(statement).all()
    
    result = []
    for issue in issues:
        employee = None
        if issue.assigned_to:
            employee = session.get(Employee, issue.assigned_to)
        
        result.append({
            "id": issue.id,
            "description": issue.description,
            "department": issue.department,
            "priority": issue.priority,
            "status": issue.status,
            "created_at": str(issue.created_at),
            "assigned_to_id": issue.assigned_to,
            "assigned_to_name": employee.name if employee else None,
            "assigned_to_email": employee.email if employee else None,
        })
    
    return result

@router.get("/send-test-email")
def send_test_email():
    """
    Send a test email to verify SMTP configuration.
    """
    from app.services.email_service import EmailService
    
    test_email = "mohammedrawan653@gmail.com"
    subject = "🧪 Test Email from ZEdny AI System"
    content = """
    Hello!
    
    This is a TEST email from your ZEdny AI Customer Service System.
    
    If you are receiving this, it means:
    ✅ The email service is working correctly
    ✅ Your email address is registered in the system
    ✅ Future escalation notifications will be sent to this address
    
    Next steps:
    - Try escalating a customer inquiry in the chat
    - You should receive an email with the issue details
    
    Best regards,
    ZEdny AI Team
    """
    
    EmailService.send_notification(test_email, subject, content)
    
    return {
        "status": "sent",
        "message": f"Test email sent to {test_email}. Check console logs or inbox.",
        "note": "If you see 'MOCK EMAIL', configure SMTP credentials in .env"
    }
