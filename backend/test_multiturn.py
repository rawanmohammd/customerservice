import requests
import uuid
import time

API_URL = "http://localhost:8000/api/chat/"

def chat(message, session_id):
    print(f"\n👤 User: {message}")
    response = requests.post(API_URL, json={"message": message, "session_id": session_id})
    if response.status_code == 200:
        res_data = response.json()
        print(f"🤖 AI: {res_data['text']}")
        print(f"   [Action: {res_data['action']}]")
        if res_data.get('escalation', {}).get('escalated'):
             print(f"   🚨 ESCALATED to {res_data['escalation'].get('department')} (Priority: {res_data['escalation'].get('priority')})")
        return res_data
    else:
        print(f"❌ Error: {response.status_code}")
        return None

def run_scenario():
    session_id = str(uuid.uuid4())
    print(f"--- Starting Session: {session_id} ---")
    
    # Message 1: Vague
    chat("عندي مشكلة في الموقع مش شغال", session_id)
    time.sleep(2)
    
    # Message 2: Providing partial info
    chat("بيطلع رسالة خطأ 500 لما بدوس على الدخول", session_id)
    time.sleep(2)
    
    # Message 3: Providing urgency/final context
    chat("الموضوع دا واقف بسببه الشغل كله بقاله ساعتين", session_id)

if __name__ == "__main__":
    run_scenario()
