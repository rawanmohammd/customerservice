from typing import Dict, Any
from sqlmodel import Session
from .vector_service import VectorService
from .dummy_rag import MockRAG
from .llm_service import LLMService

class AIService:
    """
    The Brain of the backend.
    """

    @classmethod
    def process_message(cls, message: str, session_id: str, db_session: Session) -> Dict[str, Any]:
        """
        1. Save User Message to History
        2. Check for explicit "Escalate" intent or RAG match.
        3. If no simple answer, use LLM to decide: Follow-up OR Escalate.
        """
        from app.models.models import ChatMessage
        import json

        # 1. Save User Message
        user_msg = ChatMessage(session_id=session_id, role="user", content=message)
        db_session.add(user_msg)
        db_session.commit()

        # 2. Get History
        from sqlmodel import select
        statement = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
        history_objs = db_session.exec(statement).all()
        history = [{"role": m.role, "content": m.content} for m in history_objs]

        message_lower = message.lower()
        
        # 0. Check if user is explicitly asking for human
        force_escalate = any(w in message_lower for w in ["human", "agent", "didn't work", "not helpful", "escalate", "speak to"])
        
        if not force_escalate:
            # 1. Semantic Search (RAG)
            vector_result = VectorService.search(message, threshold=0.2)
            
            if vector_result and vector_result["score"] > 0.82:
                answer_text = vector_result["doc"]["text"]
                # Save AI Response
                ai_msg = ChatMessage(session_id=session_id, role="assistant", content=answer_text)
                db_session.add(ai_msg)
                db_session.commit()
                
                return {
                    "action": "reply",
                    "text": answer_text,
                    "source": "vector_db",
                    "confidence": vector_result["score"]
                }
        
        # 2. Multi-turn Brain: Decide next step
        decision = LLMService.decide_next_step(history)
        
        if decision["action"] == "escalate" or force_escalate:
            # Full classification for the final report
            classification = LLMService.classify_message(message)
            
            escalation_text = decision.get("text", "I am forwarding your request to our team.")
            if force_escalate:
                 escalation_text = "I understand you'd like to speak with a human. I'm escalating this to our team right away."

            # Save AI Response
            ai_msg = ChatMessage(session_id=session_id, role="assistant", content=escalation_text)
            db_session.add(ai_msg)
            db_session.commit()

            return {
                "action": "escalate",
                "report": {
                    "summary": classification["summary"],
                    "department": classification["department"],
                    "priority": classification["priority"],
                    "extracted_info": classification["technical_details"],
                    "suggested_fix": "Investigate conversation history and logs."
                },
                "text": escalation_text
            }
        
        # 3. Handle Questioning or Generic Answer
        reply_text = decision["text"]
        ai_msg = ChatMessage(session_id=session_id, role="assistant", content=reply_text)
        db_session.add(ai_msg)
        db_session.commit()

        return {
            "action": "reply",
            "text": reply_text
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
