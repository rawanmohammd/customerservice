from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os

class VectorService:
    _model = None
    _kb_vectors = None
    _kb_data = []

    @classmethod
    def load_kb(cls):
        """Load Knowledge Base from JSON file."""
        try:
            # Path to knowledge_base.json in app/core/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            kb_path = os.path.join(base_dir, 'core', 'knowledge_base.json')
            
            if os.path.exists(kb_path):
                with open(kb_path, 'r', encoding='utf-8') as f:
                    cls._kb_data = json.load(f)
                print(f"📚 Loaded {len(cls._kb_data)} FAQs from knowledge_base.json")
            else:
                print(f"⚠️ Warning: knowledge_base.json not found at {kb_path}. Using empty KB.")
                cls._kb_data = []
        except Exception as e:
            print(f"❌ Error loading KB: {e}")
            cls._kb_data = []

    @classmethod
    def get_model(cls):
        """Lazy load the model to avoid heavy startup if not used."""
        if cls._model is None:
            # 1. Load Data
            cls.load_kb()
            
            # Model Selection for Free Tier Deployment:
            # - 'all-MiniLM-L6-v2': Lightweight (80MB), Fast, Good for Demo (Free Servers)
            # - 'thenlper/gte-large': Production Grade (1GB+), High Memory
            
            # Using MiniLM for lighter footprint on free Render/Railway instances
            model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
            print(f"⏳ Loading AI Model ({model_name})...")
            cls._model = SentenceTransformer(model_name)
            
            # 2. Index the Knowledge Base
            if cls._kb_data:
                texts = [doc['text'] for doc in cls._kb_data]
                cls._kb_vectors = cls._model.encode(texts)
                print(f"✅ AI Model Loaded & {len(cls._kb_data)} FAQs Indexed.")
            else:
                print("⚠️ Knowledge Base is empty. No vectors indexed.")
                cls._kb_vectors = np.array([])
                
        return cls._model

    @classmethod
    def search(cls, query: str, threshold: float = 0.35) -> Dict[str, Any] | None:
        """
        Performs Hybrid Search:
        1. Semantic Search (Vector Cosine Similarity)
        2. Keyword Boosting (+0.15 score if keywords match)
        """
        model = cls.get_model()
        
        if not cls._kb_data:
            return None
        
        # 1. Vector Search
        query_vec = model.encode([query])
        similarities = cosine_similarity(query_vec, cls._kb_vectors)[0]
        
        # 2. Keyword Boosting Logic
        query_lower = query.lower()
        boosted_scores = similarities.copy()
        
        for idx, doc in enumerate(cls._kb_data):
            keywords = doc.get("keywords", [])
            # If ANY keyword exists in the query, boost the score
            if any(k.lower() in query_lower for k in keywords):
                # Apply a significant boost for keyword matches
                # This helps resolving specific technical errors code or product names
                boosted_scores[idx] += 0.15
        
        # 3. Find Best Match
        best_idx = np.argmax(boosted_scores)
        best_score = boosted_scores[best_idx]
        
        # doc = cls._kb_data[best_idx]
        # print(f"🔍 Hybrid Search: '{query}' -> Match: '{doc['text'][:30]}...' (Score: {best_score:.4f})")
        
        if best_score >= threshold:
            return {
                "doc": cls._kb_data[best_idx],
                "score": float(best_score)
            }
        
        return None
