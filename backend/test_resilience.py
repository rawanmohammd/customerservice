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

def test_topic_pivot_layla():
    print("\n" + "="*60)
    print("STRESS TEST: Layla (The Pivot Master)")
    print("Goal: Pivot from Sales -> Technical Support -> Company Info -> User Frustration.")
    print("="*60)
    sid = str(uuid.uuid4())
    
    # turn 1: Sales/Pricing
    chat(sid, "Hello, I'm interested in your Web Development packages. How much do you charge for a startup site?", "Layla")
    time.sleep(2)
    
    # turn 2: Abrupt pivot to technical bug
    chat(sid, "Actually, wait. My friend is using your service and says his login button is broken on Safari. Can you fix it?", "Layla")
    time.sleep(2)
    
    # turn 3: Pivot to Location / Hours
    chat(sid, "Nevermind the bug for now. I want to visit your office tomorrow to discuss a contract. Where are you and what time do you open?", "Layla")
    time.sleep(2)
    
    # turn 4: Frustration / Grounding test
    chat(sid, "You're just a bot, aren't you? You didn't even answer my pricing question properly.", "Layla")

def test_grounding_reasoning_karem():
    print("\n" + "="*60)
    print("STRESS TEST: Karem (The Reasoning Test)")
    print("Goal: Test if AI 'understands' logic or just 'retrieves' text.")
    print("="*60)
    sid = str(uuid.uuid4())
    
    # turn 1: Contextual question
    chat(sid, "Does ZEdny work on weekends?", "Karem")
    time.sleep(2)
    
    # turn 2: Logic test (If I visit on Friday morning, will someone be there?)
    chat(sid, "So if I show up at your New Cairo office this Friday at 10 AM, will I find anyone to talk to?", "Karem")
    time.sleep(2)
    
    # turn 3: Reasoning (If a project takes 4-6 weeks, and I start today Jan 2nd, when is the EARLIEST I can go live?)
    chat(sid, "If I sign a contract for a corporate site today (Jan 2nd), and your timeline is 4-6 weeks, can I launch by February 1st?", "Karem")

if __name__ == "__main__":
    print("🚀 Starting Intelligence & Resilience Audit on Production...")
    test_topic_pivot_layla()
    test_grounding_reasoning_karem()
    print("\n✅ Audit Complete. Analyze results above.")
