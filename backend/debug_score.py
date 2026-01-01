from app.services.vector_service import VectorService
import numpy as np

def debug():
    query = "Can you fix my printer?"
    print(f"🔎 DEBUGGING QUERY: '{query}'")
    
    # Force load checks
    VectorService.load_kb()
    model = VectorService.get_model()
    
    # 1. Vector Score
    query_vec = model.encode([query])
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity(query_vec, VectorService._kb_vectors)[0]
    
    # 2. Hybrid Logic
    query_lower = query.lower()
    boosted_scores = similarities.copy()
    
    best_idx = -1
    best_score = -1.0
    
    # Look for ID 101 specifically
    target_id = 101
    target_idx = -1
    
    for idx, doc in enumerate(VectorService._kb_data):
        if doc['id'] == target_id:
            target_idx = idx
            
        keywords = doc.get("keywords", [])
        boost = 0
        if any(k.lower() in query_lower for k in keywords):
            boost = 0.15
            boosted_scores[idx] += boost
            
        if boosted_scores[idx] > best_score:
            best_score = boosted_scores[idx]
            best_idx = idx
            
    print(f"\n🏆 BEST MATH:")
    best_doc = VectorService._kb_data[best_idx]
    print(f"ID: {best_doc.get('id')}")
    print(f"Text: {best_doc['text']}")
    print(f"Base Score: {similarities[best_idx]:.4f}")
    print(f"Final Score: {best_score:.4f}")
    
    print(f"\n🎯 TARGET MATCH (ID 101):")
    if target_idx != -1:
        target_doc = VectorService._kb_data[target_idx]
        print(f"Text: {target_doc['text']}")
        print(f"Keywords: {target_doc.get('keywords')}")
        print(f"Base Score: {similarities[target_idx]:.4f}")
        print(f"Final Score: {boosted_scores[target_idx]:.4f}")
        
        # Check why keyword didn't match if score is low
        matches = [k for k in target_doc.get('keywords', []) if k.lower() in query_lower]
        print(f"Matched Keywords: {matches}")
    else:
        print("❌ ID 101 NOT FOUND IN KB")

if __name__ == "__main__":
    debug()
