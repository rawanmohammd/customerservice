import requests
import json
from datetime import datetime

# API Endpoint - Using Localhost for verification
API_URL = "http://localhost:8000/api/chat/"
TIMEOUT = 120  # Increased for slow local LLM

# Test Cases
test_cases = [
    {
        "id": 1,
        "category": "Ambiguous",
        "message": "الموقع بطيء جداً، وأحياناً البوت مش بيرد. محتاج حل سريع.",
        "expected": {
            "department": ["web", "ai"],
            "priority": ["medium", "high"]
        }
    },
    {
        "id": 2,
        "category": "Very Generic",
        "message": "عندنا مشكلة كبيرة في النظام. ممكن حد يساعدنا؟",
        "expected": {
            "department": ["general"],
            "priority": ["medium"]
        }
    },
    {
        "id": 3,
        "category": "Multi-Department",
        "message": "الشات بوت مش بيرد زي الأول، وكمان الموقع بيطلع error 404 لما أدوس على صفحة المنتجات. محتاجين نصلح ده قبل إطلاق الكامبين بكرة.",
        "expected": {
            "department": ["web", "ai"],
            "priority": ["high"]
        }
    },
    {
        "id": 4,
        "category": "Operations + Commercial",
        "message": "عندنا 500 طلب معلقين في السيستم، والتحصيل متوقف. الكلاينت زعلانين جداً وبيهددوا بإلغاء العقد.",
        "expected": {
            "department": ["operations", "commercial"],
            "priority": ["high"]
        }
    },
    {
        "id": 5,
        "category": "Not Urgent Feature",
        "message": "نفسي نضيف feature جديدة للموقع: فلترة المنتجات حسب السعر. مش مستعجل بس لو تقدروا تعملوها خلال الشهر الجاي هيبقى رائع.",
        "expected": {
            "department": ["web"],
            "priority": ["low", "medium"]
        }
    },
    {
        "id": 6,
        "category": "Fake Urgency",
        "message": "URGENT URGENT!! محتاج أغير باسورد الحساب بتاعي بس نسيت الإيميل!",
        "expected": {
            "department": ["general"],
            "priority": ["low", "medium"]
        }
    },
    {
        "id": 7,
        "category": "Egyptian Dialect",
        "message": "يا عم الموقع واقف خالص، مفيش حاجة بتفتح. دا إحنا بنخسر فلوس كتير كل دقيقة!",
        "expected": {
            "department": ["web"],
            "priority": ["high"]
        }
    },
    {
        "id": 8,
        "category": "Arabic + English Mix",
        "message": "الـ AI model بتاعنا مش accurate، بيطلع results غلط في 40% من الحالات. ده بيأثر على الـ user experience بشكل سلبي.",
        "expected": {
            "department": ["ai"],
            "priority": ["high"]
        }
    },
    {
        "id": 9,
        "category": "Very Long Query",
        "message": "السلام عليكم، أنا صاحب شركة تسويق إلكتروني وعندي مشكلة معقدة شوية. إحنا استخدمنا الموقع بتاعكم من 6 شهور، وكان شغال تمام، بس من أسبوعين بدأنا نلاحظ إن الـ chatbot مش بيفهم أسئلة العملاء زي زمان. مثلاً، لما عميل يسأل عن سعر منتج معين، البوت بيرد بحاجات مالهاش علاقة. جربنا نعمل refresh للصفحة، جربنا متصفحات تانية، نفس المشكلة. ده بيأثر على المبيعات بتاعتنا جداً. ممكن حد يساعدنا نحل المشكلة دي بسرعة لأن عندنا عرض كبير هيبدأ الأسبوع الجاي؟",
        "expected": {
            "department": ["ai"],
            "priority": ["high"]
        }
    },
    {
        "id": 10,
        "category": "No Context",
        "message": "مش شغال",
        "expected": {
            "department": ["general"],
            "priority": ["low", "medium"]
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
            json={"message": test_case['message']},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract classification
            department = result.get("escalation", {}).get("department", "N/A")
            priority = result.get("escalation", {}).get("priority", "N/A")
            escalated = result.get("escalation", {}).get("escalated", False)
            
            # Check results
            dept_correct = department in test_case["expected"]["department"]
            priority_correct = priority in test_case["expected"]["priority"]
            
            print(f"\n✅ Response received")
            print(f"Department: {department} {'✅' if dept_correct else '❌'}")
            print(f"Priority: {priority} {'✅' if priority_correct else '❌'}")
            print(f"Escalated: {escalated}")
            print(f"\nAI Response Preview:")
            print(result.get("text", "")[:200] + "...")
            
            return {
                "test_id": test_case['id'],
                "category": test_case['category'],
                "department_actual": department,
                "department_expected": test_case["expected"]["department"],
                "department_correct": dept_correct,
                "priority_actual": priority,
                "priority_expected": test_case["expected"]["priority"],
                "priority_correct": priority_correct,
                "escalated": escalated,
                "status": "PASS" if (dept_correct and priority_correct) else "FAIL"
            }
        else:
            print(f"❌ API Error: {response.status_code}")
            return {
                "test_id": test_case['id'],
                "status": "ERROR",
                "error": f"HTTP {response.status_code}"
            }
            
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
        if r.get("status") == "PASS":
            print(f"\n✅ Test #{r['test_id']}: {r['category']}")
            print(f"   Department: {r['department_actual']} (Expected: {r['department_expected']})")
            print(f"   Priority: {r['priority_actual']} (Expected: {r['priority_expected']})")
        elif r.get("status") == "FAIL":
            print(f"\n❌ Test #{r['test_id']}: {r['category']}")
            print(f"   Department: {r['department_actual']} ❌ (Expected: {r['department_expected']})")
            print(f"   Priority: {r['priority_actual']} {'✅' if r['priority_correct'] else '❌'} (Expected: {r['priority_expected']})")
        else:
            print(f"\n⚠️  Test #{r['test_id']}: ERROR - {r.get('error')}")
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
