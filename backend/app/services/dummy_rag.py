from typing import List, Dict

class MockRAG:
    """
    Simulates a RAG (Retrieval-Augmented Generation) system.
    In a real system, this would modify embeddings and query a Vector DB (e.g., Pinecone/Chroma).
    Here we use a simple keyword matcher for the prototype.
    """

    KNOWLEDGE_BASE = [
        {
            "id": 1,
            "category": "auth",
            "keywords": ["login", "password", "sign in", "cant login", "forgot", "reset"],
            "solution": "To reset your password, click 'Forgot Password' on the login page. A reset link will be sent to your registered email.",
            "is_technical": False
        },
        {
            "id": 6,
            "category": "subscription",
            "keywords": ["gold plan", "silver plan", "upgrade", "subscription", "features"],
            "solution": "Our Gold Plan includes 24/7 Priority Support, dedicated AI servers, and unlimited API calls. Silver Plan includes business hours support and shared resources.",
            "is_technical": False
        },
        {
            "id": 7,
            "category": "refund",
            "keywords": ["refund", "money back", "cancel", "cancellation"],
            "solution": "You can cancel your subscription at any time from the settings. Refunds are processed within 5-7 business days for the unused portion of the month.",
            "is_technical": False
        },
        {
            "id": 2,
            "category": "pricing",
            "keywords": ["price", "cost", "how much", "expensive", "quote"],
            "solution": "Our pricing depends on the project scope. For Web Development, we start at $1000. AI solutions require a custom consultation.",
            "is_technical": False
        },
        {
            "id": 4,
            "category": "about",
            "keywords": ["who are you", "what is zedny", "about company", "what do you do"],
            "solution": "ZEdny is a leading AI & Software Solutions provider. We specialize in building intelligent web platforms, automated workflows, and custom AI agents for enterprises.",
            "is_technical": False
        },
        {
            "id": 5,
            "category": "location",
            "keywords": ["location", "where", "address", "office", "contact"],
            "solution": "We are located in Cairo, Egypt. You can contact us at hello@zedny.com or visit our HQ in New Cairo.",
            "is_technical": False
        },
        {
            "id": 3,
            "category": "api",
            "keywords": ["api", "key", "token", "auth header", "401"],
            "solution": "Ensure you are including the 'Authorization: Bearer <TOKEN>' header. API keys can be generated in the Settings dashboard.",
            "is_technical": True
        }
    ]

    @staticmethod
    def search(query: str) -> Dict | None:
        """
        Naive search implementation with basic word boundary check.
        Returns the best matching doc or None.
        """
        query_lower = f" {query.lower()} " # Pad with spaces for boundary check
        
        best_match = None
        max_score = 0

        for doc in MockRAG.KNOWLEDGE_BASE:
            score = 0
            for keyword in doc["keywords"]:
                # Check for exact word: " where " in " ... everywhere ... " -> False
                if f" {keyword} " in query_lower:
                    score += 1
            
            if score > max_score:
                max_score = score
                best_match = doc

        # Only return if at least one keyword matched
        return best_match if max_score > 0 else None
