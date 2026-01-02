import requests
import json
from datetime import datetime

# API Endpoint - Using Hugging Face deployment
API_URL = "https://rawanpo-zedny-ai.hf.space/api/chat/"
TIMEOUT = 120  # 2 minutes for slow LLM responses

# Test Cases
test_cases = [
    {
        "id": 1,
        "category": "RAG - Password Reset",
        "message": "I forgot my password, how can I reset it?",
        "expected": {
            "action": "reply",
            "contains": "Forgot Password"
        }
    },
    {
        "id": 2,
        "category": "RAG - Company Location",
        "message": "Where is ZEdny HQ located?",
        "expected": {
            "action": "reply",
            "contains": "New Cairo"
        }
    },
    {
        "id": 3,
        "category": "RAG - Business Hours",
        "message": "What are your working hours?",
        "expected": {
            "action": "reply",
            "contains": "Sunday to Thursday"
        }
    },
    {
        "id": 4,
        "category": "RAG - Timeline",
        "message": "How long does a corporate website take?",
        "expected": {
            "action": "reply",
            "contains": "4-6 weeks"
        }
    },
    {
        "id": 5,
        "category": "Department - Web Bug",
        "message": "The login button is not clicking on mobile Chrome.",
        "expected": {
            "department": ["web"],
            "priority": ["high", "medium"]
        }
    },
    {
        "id": 6,
        "category": "Department - AI Service",
        "message": "We want to build a custom recommendation model for our e-commerce.",
        "expected": {
            "department": ["ai"],
            "priority": ["medium", "low"]
        }
    },
    {
        "id": 7,
        "category": "Department - Commercial/Billing",
        "message": "I want to upgrade my plan and need the bank transfer details.",
        "expected": {
            "department": ["commercial"],
            "priority": ["medium", "high"]
        }
    },
    {
        "id": 8,
        "category": "Ambiguous/Multi-turn",
        "message": "It's not working",
        "expected": {
            "action": "reply", # Should ask clarifying question
            "contains": "specify"
        }
    },
    {
        "id": 9,
        "category": "Department - Operations",
        "message": "The delivery tracking for my hardware order is stuck.",
        "expected": {
            "department": ["operations"],
            "priority": ["high", "medium"]
        }
    },
    {
        "id": 10,
        "category": "Dialect - Egyptian",
        "message": "الموقع واقع خالص يا جماعة، إلحقونا.",
        "expected": {
            "department": ["web"],
            "priority": ["high"]
        }
    },
    {
        "id": 11,
        "category": "Long Technical Query",
        "message": "Our React frontend is showing a hydration error specifically in the production build on Vercel, but works fine locally. We upgraded to Next.js 14 and since then the AI widget is causing mismatches.",
        "expected": {
            "department": ["web", "ai"],
            "priority": ["high"]
        }
    },
    {
        "id": 12,
        "category": "RAG - Maintenance",
        "message": "Do you provide support after the project is live?",
        "expected": {
            "action": "reply",
            "contains": "post-launch support"
        }
    },
    {
        "id": 13,
        "category": "Department - General/HR",
        "message": "Are you guys hiring for software engineers?",
        "expected": {
            "department": ["general"],
            "priority": ["low"]
        }
    },
    {
        "id": 14,
        "category": "Commercial - High Value",
        "message": "We are a Fortune 500 company looking for an enterprise contract for 1000 users.",
        "expected": {
            "department": ["commercial"],
            "priority": ["high"]
        }
    },
    {
        "id": 15,
        "category": "Sarcasm/Complaint",
        "message": "Oh great, the site is down again on a Friday night. Amazing service.",
        "expected": {
            "department": ["web"],
            "priority": ["high"]
        }
    }
]

def run_test(test_case):
    """Run a single test case"""
    print(f"\n{'='*80}")
    print(f"Test #{test_case['id']}: {test_case['category']}")
    print(f"{'='*80}")
    print(f"Message: {test_case['message'][:100]}...")
    
    try:
        # Send request
        response = requests.post(
            API_URL,
            json={"message": test_case['message'], "session_id": "test-suite"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            
            action_actual = result.get("action")
            text_actual = result.get("text", "")
            
            is_correct = False
            
            # Check Action based testing (RAG/Ambiguous)
            if "action" in test_case["expected"]:
                action_match = action_actual == test_case["expected"]["action"]
                content_match = test_case["expected"]["contains"].lower() in text_actual.lower() if "contains" in test_case["expected"] else True
                is_correct = action_match and content_match
                
                print(f"\n✅ Response received")
                print(f"Action: {action_actual} {'✅' if action_match else '❌'} (Expected: {test_case['expected']['action']})")
                if "contains" in test_case["expected"]:
                    print(f"Content Match: {'✅' if content_match else '❌'} (Searched: '{test_case['expected']['contains']}')")
            
            # Check Escalation based testing (Departments)
            else:
                department = result.get("escalation", {}).get("department", "N/A")
                priority = result.get("escalation", {}).get("priority", "N/A")
                
                dept_correct = department in test_case["expected"]["department"]
                priority_correct = priority in test_case["expected"]["priority"]
                is_correct = dept_correct and priority_correct
                
                print(f"\n✅ Response received")
                print(f"Department: {department} {'✅' if dept_correct else '❌'}")
                print(f"Priority: {priority} {'✅' if priority_correct else '❌'}")
            
            print(f"\nAI Response Preview:")
            print(text_actual[:200] + "...")
            
            return {
                "test_id": test_case['id'],
                "category": test_case['category'],
                "status": "PASS" if is_correct else "FAIL",
                "actual": result
            }
        else:
            print(f"❌ API Error: {response.status_code}")
            return {"test_id": test_case['id'], "status": "ERROR", "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return {
            "test_id": test_case['id'],
            "status": "ERROR",
            "error": str(e)
        }

def main():
    """Run all tests and generate report"""
    print("\n" + "="*80)
    print("🧪 ZEdny AI Chatbot - Automated Testing Suite")
    print("="*80)
    
    results = []
    for test_case in test_cases:
        result = run_test(test_case)
        results.append(result)
    
    # Generate Summary
    print("\n\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    errors = sum(1 for r in results if r.get("status") == "ERROR")
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Errors: {errors}")
    print(f"\nSuccess Rate: {(passed/len(results)*100):.1f}%")
    
    # Detailed Results
    print("\n" + "="*80)
    print("📋 DETAILED RESULTS")
    print("="*80)
    
    for r in results:
        status_icon = "✅" if r.get("status") == "PASS" else "❌" if r.get("status") == "FAIL" else "⚠️"
        print(f"\n{status_icon} Test #{r['test_id']}: {r['category']}")
        if r.get("status") == "ERROR":
            print(f"   Error: {r.get('error')}")
        else:
            actual = r.get("actual", {})
            action = actual.get("action")
            print(f"   AI Action: {action}")
            if action == "escalate":
                esc = actual.get("escalation", {})
                print(f"   Escalated To: {esc.get('department')} (Priority: {esc.get('priority')})")
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_prod_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
