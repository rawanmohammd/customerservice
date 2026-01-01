from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.ai_service import AIService
from sqlmodel import Session
from app.core.database import get_session
from app.services.assignment_service import AssignmentService
from app.models.models import Issue, Client

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "guest"
    client_email: Optional[str] = None

class ChatResponse(BaseModel):
    action: str  # 'reply' or 'escalate'
    text: str
    report: Optional[Dict[str, Any]] = None

from app.services.email_service import EmailService

@router.post("/", response_model=ChatResponse)
async def chat_interaction(request: ChatRequest, session: Session = Depends(get_session)):
    """
    User talks to AI.
    - Scans Knowledge Base.
    - If capable, replies.
    - If complex, escalates -> Creates Issue in DB -> Assigns Employee.
    """
    try:
        # 1. AI Analysis
        ai_response = AIService.process_message(request.message)
        
        # 2. If Escalate, Save to DB
        if ai_response["action"] == "escalate":
            report = ai_response["report"]
            
            # Find best employee
            assigned_emp = AssignmentService.assign_employee(
                session, 
                report["department"], 
                report["priority"]
            )
            
            # Create Issue Record
            new_issue = Issue(
                description=report["summary"],
                department=report["department"],
                priority=report["priority"],
                status="open",
                ai_summary=str(report["extracted_info"]),
                assigned_to=assigned_emp.id if assigned_emp else None,
                client_id=None # Connect to real client if exists
            )
            session.add(new_issue)
            session.commit()
            
            # 3. NOTIFY via Email (If High Priority)
            # 3. NOTIFY via Email (For ALL escalations during demo)
            print(f"DEBUG: Checking email logic. Priority: {report['priority']}, Assigned: {assigned_emp}")
            if assigned_emp:
                email_body = EmailService.generate_html_report(report)
                EmailService.send_notification(
                    to_email=assigned_emp.email,
                    subject=f"📢 New Issue: {report['department']} - Priority: {report['priority'].upper()}",
                    content=email_body
                )
                ai_response["text"] += f"\n\n(Notification: Email sent to {assigned_emp.name})"
            
            # Append assignment info to response (for demo purpose)
            elif assigned_emp:
                ai_response["text"] += f"\n\n(Internal: Assigned to {assigned_emp.name} in {assigned_emp.department})"
        
        return ai_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
