import sys
import os
from sqlmodel import Session, select

# Add BACKEND directory to path (so 'app' is top-level)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from app.services.ai_service import AIService
from app.services.assignment_service import AssignmentService
from app.core.database import engine
from app.models.models import Employee

def test_full_flow():
    print("\n--- 🤖 Testing AI + Database Routing Flow ---\n")
    
    # 1. Simulate User Message
    user_message = "I need a new landing page for my e-commerce site. It's urgent!"
    print(f"📩 User Message: \"{user_message}\"")
    
    # 2. AI Processing
    print("🧠 AI Analyzing Intent...")
    ai_response = AIService.process_message(user_message)
    
    if ai_response["action"] == "escalate":
        report = ai_response["report"]
        dept = report["department"]
        priority = report["priority"]
        
        print(f"✅ AI Classification: Department='{dept}', Priority='{priority}'")
        
        # 3. Database Assignment
        print("🔍 Searching Database for Best Employee...")
        with Session(engine) as session:
            assigned_emp = AssignmentService.assign_employee(session, dept, priority)
            
            if assigned_emp:
                print(f"🎉 ASSIGNED: {assigned_emp.name}")
                print(f"   - Role: {assigned_emp.role}")
                print(f"   - Email: {assigned_emp.email}")
                print(f"   - Reasoning: Selected from '{dept}' department" + (" (Senior prioritised)" if priority == "high" else ""))
            else:
                print("❌ No suitable employee found.")
    else:
        print(f"ℹ️ AI Solved it directly: {ai_response['text']}")

    print("\n-----------------------------------------------\n")
    
    # Test 2: AI Request
    user_message_2 = "Can you build a chatbot?"
    print(f"📩 User Message: \"{user_message_2}\"")
    ai_response_2 = AIService.process_message(user_message_2)
    
    if ai_response_2["action"] == "escalate":
         with Session(engine) as session:
            emp = AssignmentService.assign_employee(session, ai_response_2["report"]["department"], "medium")
            print(f"🎉 ASSIGNED: {emp.name} ({emp.department})")

if __name__ == "__main__":
    test_full_flow()
