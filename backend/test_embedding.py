import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from app.services.vector_service import VectorService

def benchmark_embedding_upgrade():
    """
    Test semantic search accuracy before/after embedding upgrade.
    """
    
    test_queries = [
        ("I want my money back", "Refunds can be requested"),  # Should match refund FAQ
        ("Where is your office?", "ZEdny Company HQ"),  # Should match location FAQ  
        ("Reset my password", "For password reset"),  # Should match auth FAQ
        ("My server crashed with 500 error", "Error 500 or Internal"),  # Technical match
        ("How do I contact you?", "hello@zedny.com"),  # Contact info
    ]
    
    print("\n🧪 EMBEDDING MODEL BENCHMARK")
    print("="*80)
    print(f"Model: gte-large (1024-dim)")
    print(f"FAQs: {len(VectorService._kb_data)}")
    print("="*80)
    
    for query, expected_match in test_queries:
        print(f"\n📝 Query: \"{query}\"")
        print(f"   Expected Match: \"{expected_match}...\"")
        
        result = VectorService.search(query, threshold=0.2)
        
        if result:
            matched_text = result['doc']['text']
            score = result['score']
            
            is_correct = expected_match.lower() in matched_text.lower()
            status = "✅" if is_correct else "❌"
            
            print(f"   {status} Match: \"{matched_text[:60]}...\"")
            print(f"   Score: {score:.4f}")
        else:
            print(f"   ❌ No match found")
        
        print("-" * 80)

if __name__ == "__main__":
    benchmark_embedding_upgrade()
