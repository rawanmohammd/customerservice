import sys
import os
from fastapi.testclient import TestClient

# Add BACKEND to path so 'app' is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from main import app

client = TestClient(app)

def test_api_flow():
    print("\n--- 🌐 Testing FastAPI Endpoints (TestClient) ---\n")
    
    # 1. Test Root
    response = client.get("/")
    print(f"GET / -> Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 200
    
    # 2. Test Chat (Simple FAQ)
    print("\n👉 Testing /api/chat (FAQ)...")
    chat_payload = {"message": "How much does it cost?", "user_id": "test_user"}
    response = client.post("/api/chat/", json=chat_payload)
    print(f"POST /api/chat -> Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["action"] == "reply"

    # 3. Test Chat (Escalation)
    print("\n👉 Testing /api/chat (Escalation to Web)...")
    escalate_payload = {
        "message": "My website is down! Error 500 everywhere. This is urgent!", 
        "user_id": "urgent_user"
    }
    response = client.post("/api/chat/", json=escalate_payload)
    print(f"POST /api/chat -> Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert data["action"] == "escalate"
    # Check for Email Alert text which confirms EmailService was called
    assert "Alert: An urgent email has been sent" in data["text"] 
    print("✅ Email Notification Triggered!")

    # 4. Test Issues List (Did it save to DB?)
    print("\n👉 Testing /api/issues (Verification)...")
    response = client.get("/api/issues/")
    print(f"GET /api/issues -> Status: {response.status_code}")
    issues = response.json()
    print(f"Issues Found: {len(issues)}")
    print(f"Latest Issue: {issues[-1] if issues else 'None'}")
    
    assert response.status_code == 200
    assert len(issues) > 0
    assert issues[-1]["priority"] == "high"

    print("\n✅ API Flow Verification Successful!")

if __name__ == "__main__":
    test_api_flow()
