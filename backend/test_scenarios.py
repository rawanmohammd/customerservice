import sys
import os
from fastapi.testclient import TestClient

# Add BACKEND to path so 'app' is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from main import app

client = TestClient(app)

def run_scenario(name, message, expected_action, expected_dept=None, expected_priority=None):
    print(f"\n🧪 SCENARIO: {name}")
    print(f"   Input: '{message}'")
    
    response = client.post("/api/chat/", json={"message": message, "user_id": "tester"})
    data = response.json()
    
    print(f"   Action: {data['action'].upper()}")
    
    if data['action'] == 'escalate':
        report = data['report']
        print(f"   Summary: {report['summary']}")
        print(f"   Department: {report['department'].upper()}")
        print(f"   Priority: {report['priority'].upper()}")
        
        # Validation
        if expected_dept:
            assert report['department'] == expected_dept, f"Expected {expected_dept}, got {report['department']}"
        if expected_priority:
            assert report['priority'] == expected_priority, f"Expected {expected_priority}, got {report['priority']}"
            
    # Main Validation
    assert data['action'] == expected_action, f"Expected {expected_action}, got {data['action']}"
    print("   ✅ PASSED")

def test_all_scenarios():
    print("\n🚀 STARTING COMPREHENSIVE AI TESTING...\n")

    # 1. Project Management (Client Persona)
    run_scenario(
        name="Project Timeline",
        message="How long does it take to build a custom web app?",
        expected_action="reply" # Should match "Project timelines vary..."
    )

    # 2. Maintenance (RAG)
    run_scenario(
        name="Maintenance Support",
        message="Do you provide support after the website is launched?",
        expected_action="reply" 
    )

    # 3. Explicit Escalation (User unhappy)
    run_scenario(
        name="User Forced Escalation",
        message="I need to speak to a manager immediately. This delay is unacceptable.",
        expected_action="escalate",
        expected_dept="general", 
        expected_priority="high"
    )

    # 4. Pricing / Sales (Client Inquiry)
    # RAG should handle general pricing questions if they exist in KB
    # But specific custom quotes should escalate or be handled by specific FAQs
    run_scenario(
        name="Payment Terms",
        message="Can I pay via wire transfer?",
        expected_action="reply" # Should match "We accept credit cards... wire transfers"
    )
    
    # 5. Unknown Service (Escalation)
    # Asking for something we definitely don't do
    run_scenario(
        name="Out of Scope Request",
        message="Can you fix my printer?",
        expected_action="escalate",
        expected_priority="low"
    )

    print("\n🎉 ALL SCENARIOS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all_scenarios()
