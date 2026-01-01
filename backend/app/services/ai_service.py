from typing import Dict, Any
from .vector_service import VectorService
from .dummy_rag import MockRAG
from .llm_service import LLMService

class AIService:
    """
    The Brain of the backend.
    """

    @classmethod
    def process_message(cls, message: str) -> Dict[str, Any]:
        """
        1. Semantic Search (Vector DB)
        2. If Solution Found -> Reply
        3. If Not Found -> Classify & Escalate
        """
    @classmethod
    def process_message(cls, message: str) -> Dict[str, Any]:
        """
        1. Check for explicit "Escalate/Did not work" intent.
        2. Semantic Search (RAG) - Even if urgent.
        3. If no RAG match -> Classify & Escalate.
        """
        message_lower = message.lower()
        
        # 0. Check if user is explicitly asking for human or complaining about previous answer
        # Removed "support" as it triggered false positives (e.g. "Do you provide support?")
        force_escalate = any(w in message_lower for w in ["human", "agent", "didn't work", "not helpful", "escalate", "speak to"])
        
        if not force_escalate:
            # 1. Semantic Search (The Smart Way)
            # We check RAG first, even if they say "Urgent".
            # Example: "Urgent, how do I reset password?" -> Should just answer.
            vector_result = VectorService.search(message, threshold=0.2)
            
            if vector_result:
                doc = vector_result["doc"]
                score = vector_result["score"]
                
                # If good match, return it.
                # Raised threshold to 0.82 to reduce false positives (e.g. "fix printer" matching "bug fix" at 0.81)
                if score > 0.82: 
                    return {
                        "action": "reply",
                        "text": doc["text"],
                        "source": "vector_db",
                        "confidence": score
                    }
        
        # 2. Fallback: Classify & Escalate
        # This happens if:
        # a) User forced escalation ("Human please")
        # b) RAG found nothing relevant (Score < 0.22)
        classification = LLMService.classify_message(message)
        
        return {
            "action": "escalate",
            "report": {
                "summary": classification["summary"],
                "department": classification["department"],
                "priority": classification["priority"],
                "extracted_info": classification["technical_details"],
                "suggested_fix": "Investigate logs and contacting client."
            },
            "text": "I have collected the necessary details. I am forwarding this to our " + classification["department"] + " team immediately."
        }
    
    @staticmethod
    def _mock_llm_classification(text: str) -> Dict[str, Any]:
        """
        Simulates an LLM with 'Few-Shot Prompting'.
        We act as if we gave the LLM instructions to classify and summarize.
        """
        text_lower = text.lower()
        
        # 1. Advanced Classification (Simulated)
        dept = "general"
        if any(x in text_lower for x in ["site", "web", "css", "js", "react", "frontend", "500", "slow"]):
            dept = "web"
        elif any(x in text_lower for x in ["ai", "bot", "rag", "gpt", "training", "model", "intelligence"]):
            dept = "ai"
        elif any(x in text_lower for x in ["content", "blog", "post", "seo", "article", "writing"]):
            dept = "content"
            
        # 2. Priority Detection
        priority = "medium"
        if any(x in text_lower for x in ["urgent", "crash", "immediately", "critical", "down", "human", "agent"]):
            priority = "high"
        elif "bug" not in text_lower and "error" not in text_lower:
             priority = "low"

        # 3. Smart Summarization
        # Simulating an LLM that extracts the core issue
        summary = f"[{dept.upper()}] Issue Detected: {text[:60]}..."
        if priority == "high":
            summary = f"🚨 URGENT: {summary}"

        return {
            "summary": summary,
            "department": dept,
            "priority": priority,
            "technical_details": [
                f"Detected Category: {dept.capitalize()}",
                f"Urgency Level: {priority.upper()}",
                "Action: Escalated to Specialist"
            ]
        }
