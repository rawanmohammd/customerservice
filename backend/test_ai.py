import sys
import os

# Add the project root to the python path so we can import 'backend.app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.services.ai_service import AIService

def test_ai_logic():
    print("--- Testing ZEdny AI Core ---\n")

    # Test Case 1: Simple FAQ (Should be solved by RAG)
    msg1 = "I forgot my password"
    print(f"User: {msg1}")
    response1 = AIService.process_message(msg1)
    print(f"AI Action: {response1['action']}")
    print(f"AI Response: {response1['text']}\n")
    assert response1['action'] == 'reply'

    # Test Case 2: Complex Issue (Should Escalate)
    msg2 = "My website keeps crashing when I upload large files. This is urgent."
    print(f"User: {msg2}")
    response2 = AIService.process_message(msg2)
    print(f"AI Action: {response2['action']}")
    if response2['action'] == 'escalate':
        print(f"Generated Report: {response2['report']}")
    print("\n")
    assert response2['action'] == 'escalate'
    assert response2['report']['priority'] == 'high'

    # Test Case 3: Department Routing
    msg3 = "I need an AI model that can detect cats."
    print(f"User: {msg3}")
    response3 = AIService.process_message(msg3)
    print(f"AI Action: {response3['action']}")
    if response3.get('report'):
        print(f"Routed To: {response3['report']['department']}")
    print("\n")
    assert response3['report']['department'] == 'ai'

    print("--- All Tests Passed ✅ ---")

if __name__ == "__main__":
    test_ai_logic()
