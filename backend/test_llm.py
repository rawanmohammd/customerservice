import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from app.services.llm_service import LLMService

def test_llm_classification():
    """
    Test Groq LLM with diverse scenarios to validate accuracy.
    """
    
    test_cases = [
        {
            "message": "I've been trying to reset my password for 2 hours. The link expired and my team needs urgent access to deploy our ML model. This is costing us money!",
            "expected_dept": "ai",
            "expected_priority": "high",
            "note": "Complex: Password + ML deployment + urgency"
        },
        {
            "message": "We're a Fortune 500 company evaluating vendors for our Q2 AI roadmap",
            "expected_dept": "ai",
            "expected_priority": "high",
            "note": "VIP Lead Detection"
        },
        {
            "message": "ur site is super slow, like 10 seconds to load. my boss is gonna kill me lol",
            "expected_dept": "web",
            "expected_priority": "medium",
            "note": "Casual language + non-literal urgency"
        },
        {
            "message": "I love your AI services! Can I get a discount if I also hire you for content writing?",
            "expected_dept": "general",
            "expected_priority": "high",
            "note": "Multi-service sales opportunity"
        },
        {
            "message": "Oh great, another 500 error. Just what I needed on a Friday night 🙄",
            "expected_dept": "web",
            "expected_priority": "high",
            "note": "Sarcasm detection + recurring issue"
        },
        {
            "message": "Can you write a blog post about SEO best practices?",
            "expected_dept": "content",
            "expected_priority": "low",
            "note": "Simple content request"
        },
        {
            "message": "How much does your Gold Plan cost?",
            "expected_dept": "general",
            "expected_priority": "medium",
            "note": "Sales inquiry"
        },
        {
            "message": "My React app keeps crashing on production. Error: Cannot read property 'map' of undefined",
            "expected_dept": "web",
            "expected_priority": "high",
            "note": "Technical support with stack trace"
        },
        {
            "message": "I need someone to train a custom NLP model for Arabic sentiment analysis",
            "expected_dept": "ai",
            "expected_priority": "medium",
            "note": "Specific AI service request"
        },
        {
            "message": "Where is your office located?",
            "expected_dept": "general",
            "expected_priority": "low",
            "note": "Simple informational query"
        }
    ]
    
    print("\n🧪 GROQ LLM CLASSIFICATION TEST\n" + "="*80)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['note']}")
        print(f"Message: \"{test['message']}\"")
        
        try:
            result = LLMService.classify_message(test['message'])
            
            print(f"\n✅ Result:")
            print(f"   Department: {result['department']} (Expected: {test['expected_dept']})")
            print(f"   Priority: {result['priority']} (Expected: {test['expected_priority']})")
            print(f"   Intent: {result.get('intent', 'N/A')}")
            print(f"   Summary: {result['summary']}")
            print(f"   Reasoning: {result.get('reasoning', 'N/A')}")
            
            # Validation
            dept_match = result['department'] == test['expected_dept']
            priority_match = result['priority'] == test['expected_priority']
            
            if dept_match and priority_match:
                print(f"\n✅ PASSED")
                passed += 1
            else:
                print(f"\n❌ FAILED")
                if not dept_match:
                    print(f"   ❌ Department mismatch: {result['department']} != {test['expected_dept']}")
                if not priority_match:
                    print(f"   ⚠️  Priority mismatch: {result['priority']} != {test['expected_priority']}")
                failed += 1
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            failed += 1
        
        print("-" * 80)
    
    print(f"\n📊 RESULTS: {passed}/{len(test_cases)} passed ({(passed/len(test_cases)*100):.1f}% accuracy)")
    
    if passed == len(test_cases):
        print("🎉 ALL TESTS PASSED! Groq LLM is working perfectly.")
    else:
        print(f"⚠️  {failed} tests failed. Review reasoning and adjust prompts if needed.")

if __name__ == "__main__":
    test_llm_classification()
