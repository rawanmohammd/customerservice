import requests
import uuid
import time

# Production URL
API_URL = "https://rawanpo-zedny-ai.hf.space/api/chat/"

def chat(session_id, message, persona_name):
    print(f"\n👤 [{persona_name}]: {message}")
    try:
        response = requests.post(API_URL, json={"message": message, "session_id": session_id}, timeout=120)
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 AI: {data['text']}")
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_persona_hassan():
    print("\n" + "="*50)
    print("TEST PERSONA: Hassan (Traditional/Egyptian Arabic)")
    print("Goal: Test patience and clarification on vague Egyptian query.")
    print("="*50)
    sid = str(uuid.uuid4())
    
    chat(sid, "السلام عليكم يا جماعة، الموقع بقاله يومين تقيل قوي ومش عارف أرفع عليه الصور الجديدة.", "Hassan")
    time.sleep(2)
    chat(sid, "هو أيه السبب؟ جربت من الموبايل ومن اللاب توب ونفس المشكلة.", "Hassan")
    time.sleep(2)
    chat(sid, "أنا مشترك في الباقة الكبيرة بتاعتكم، وعندي مشروع تبع شركة 'النساجون'. الموضوع دا متعطل بقاله كتير.", "Hassan")

def test_persona_sarah():
    print("\n" + "="*50)
    print("TEST PERSONA: Sarah (Technical PM / English)")
    print("Goal: Test RAG knowledge + Complex Escalation.")
    print("="*50)
    sid = str(uuid.uuid4())
    
    chat(sid, "Hello, can you tell me what is your standard timeline for a custom AI solution?", "Sarah")
    time.sleep(2)
    chat(sid, "Okay, and do you support integration with 3rd party legacy APIs? We have an old SQL system.", "Sarah")
    time.sleep(2)
    chat(sid, "We're actually seeing a 504 Gateway Timeout when our current prototype tries to hit your endpoint. Escalating this.", "Sarah")

def test_persona_omar():
    print("\n" + "="*50)
    print("TEST PERSONA: Omar (Angry Legacy Client)")
    print("Goal: Test Urgency & Human-First Escalation.")
    print("="*50)
    sid = str(uuid.uuid4())
    
    chat(sid, "SITE IS DOWN! URGENT! I want to speak to a human agent right now!", "Omar")
    time.sleep(2)
    chat(sid, "Every minute the site is down we are losing money. This is unacceptable.", "Omar")

if __name__ == "__main__":
    print("🚀 Starting Senior QA Professional Simulation on Production...")
    test_persona_hassan()
    test_persona_sarah()
    test_persona_omar()
    print("\n✅ Simulation Complete. Analyze results above.")
