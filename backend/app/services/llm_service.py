import os
import json
from typing import Dict, Any, List
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    """
    Groq LLM Service for intelligent message classification.
    Uses Llama 3.1 70B for fast, accurate analysis.
    """
    
    _client = None
    
    @classmethod
    def get_client(cls):
        """Lazy initialize Groq client"""
        if cls._client is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            cls._client = Groq(api_key=api_key)
        return cls._client

    @classmethod
    def decide_next_step(cls, history: List[Dict[str, str]], rag_context: str = None) -> Dict[str, Any]:
        """
        Analyze history and decide: Clarify, Answer, or Escalate.
        Includes RAG context to ensure AI knows company-specific info.
        """
        client = cls.get_client()
        
        system_prompt = f"""You are a smart Customer Service Coordinator for ZEdny (Software Company).
Your goal is to decide if you have enough information to either:
1. ANSWER: Giving a direct answer (Generic or using provided KNOWLEDGE BASE).
2. ESCALATE: Issue is technical/commercial and clear enough for a human.
3. ASK_QUESTION: Request is vague or missing key details.
4. ACKNOWLEDGE: Info added to an existing escalation.

=== KNOWLEDGE BASE (Use this to ANSWER if relevant) ===
{rag_context if rag_context else "No specific knowledge found for this query."}

=== LOOP PREVENTION ===
If the user already answered a question or you have asked the SAME clarification twice, do NOT ask again. ESCALATE to a human instead.

=== RULES ===
- If the user provides specific details (e.g., "Error 500", "Site down") -> action: "escalate"
- If the knowledge base has a clear answer -> action: "answer", text: "Use the info from KB"
- If it was ALREADY escalated -> action: "answer", text: "Acknowledged, I've updated the team."
- Respond in the language used by the customer (Arabic/English). Avoid over-formal language in Arabic; be helpful and natural.

Response must be ONLY valid JSON:
{{
  "action": "<ask_question|escalate|answer>",
  "text": "<The message to show to the user in their language>",
  "reasoning": "<brief intent analysis>"
}}
"""
        try:
            
            # Format history for LLM
            # history is a list of ChatMessage-like objects
            formatted_history = []
            for msg in history[-6:]: # Last 6 messages for context
                formatted_history.append({"role": msg["role"], "content": msg["content"]})

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *formatted_history
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"❌ LLM Decide Error: {str(e)}")
            return {"action": "answer", "text": "I'm having a bit of trouble processing that. Could you try rephrasing?"}

    @classmethod
    def classify_message(cls, message: str) -> Dict[str, Any]:
        # ... existing implementation ...
        """
        Analyze customer message using Groq LLM.
        Returns structured classification data.
        """
        
        system_prompt = """You are a customer service AI classifier for ZEdny, a software company offering:
- Web Development (sites, hosting, frontend/backend)
- AI Solutions (ML models, data science, AI integration)
- Content Strategy (blog writing, SEO, social media)

Analyze the customer message and respond with ONLY valid JSON (no markdown, no extra text):

{
  "department": "<web|ai|content|general>",
  "priority": "<low|medium|high>",
  "summary": "<one-line summary max 60 chars>",
  "intent": "<support|sales|complaint|inquiry>",
  "reasoning": "<brief explanation>"
}

=== CLASSIFICATION RULES ===

DEPARTMENTS:
- "web" = [Conceptual] Any technical inquiry relative to websites, web applications, frontend (UI/UX), backend (API, DB), browsers, or hosting. Includes visual bugs, functionality errors, and feature requests for web platforms.
- "ai" = [Conceptual] Any inquiry related to Artificial Intelligence, Machine Learning, Data Science, predictive models, chatbots, or data analytics.
- "commercial" = [Conceptual] Business-related inquiries involved money, contracts, account plans, billing cycles, or legal agreements.
- "operations" = [Conceptual] Logistics, shipping, delivery systems, account management, operational support, or physical infrastructure.
- "general" = [Conceptual] Non-technical inquiries about the company itself (location, hours), partnerships, or unclassified non-technical issues.

PRIORITY LEVELS:
- "high" = 
  * Urgent words: "immediately", "critical", "down", "blocking", "revenue loss"
  * VIP indicators: "Fortune 500", "enterprise", "CEO", "urgent"
  * Frustrated tone: sarcasm, repeated issues, angry language
  * Production issues: "crashed", "500 error", "site down"
  
- "medium" = 
  * Support requests without urgency
  * Bug reports affecting some users
  * Service inquiries from active customers
  
- "low" = 
  * General questions
  * Pricing inquiries
  * How-to without time pressure

INTENT:
- "sales" = wants to buy, pricing questions, service requests, discount inquiries, vendor evaluation
- "support" = has a problem, needs help, bug reports, technical issues
- "complaint" = frustrated, angry, service quality issues, repeated problems
- "inquiry" = general questions, information requests, exploring services

SPECIAL CASES:
1. Multi-topic queries (e.g., "password reset + AI model deployment") → Route to the PRIMARY issue (in this case: "web" for password blocking AI work)
2. Sarcasm/frustration (e.g., "Oh great, another error") → Treat as high priority
3. VIP/Enterprise mentions → Always high priority + "sales" intent
4. Service requests (e.g., "train a model", "write a blog") → Correct department + "sales" intent

=== TRAINING DATA (EDGE CASES) ===

Here are specific examples of how we classify ambiguous requests. Use these as your ground truth.

CASE 1: WEB vs CONTENT (The "SEO" Dilemma)
- Input: "My website is slow and Google can't see it." -> DEPT: WEB (Technical performance issue)
- Input: "I need better keywords for my blog to rank higher." -> DEPT: CONTENT (Creative strategy issue)
- Input: "Install the Yoast SEO plugin." -> DEPT: WEB (Technical task)

CASE 2: WEB vs AI (The "Chatbot" Dilemma)
- Input: "The chatbot box is covering the login button." -> DEPT: WEB (UI/Frontend issue)
- Input: "The chatbot is giving wrong answers about pricing." -> DEPT: AI (Model behavior/accuracy issue)
- Input: "I want to add a chatbot to my site." -> DEPT: AI (Service request for AI solution)

CASE 3: MEDIA/CONTENT vs WEB (The "Video" Dilemma)
- Input: "The video player is broken on Safari." -> DEPT: WEB (Technical bug)
- Input: "Can you create a promo video for our homepage?" -> DEPT: CONTENT (Media production)

CASE 4: COMMERCIAL vs GENERAL
- Input: "I want to upgrade to the Gold plan." -> DEPT: COMMERCIAL (Sales/Account)
- Input: "Where do I send the check?" -> DEPT: COMMERCIAL (Billing)
- Input: "Are you hiring?" -> DEPT: GENERAL (HR/Company)

=== FEW-SHOT EXAMPLES ===

Example 1:
Input: "I've been trying to reset my password for 2 hours. My team needs urgent access to deploy our ML model."
Output: {"department": "web", "priority": "high", "summary": "Password blocking ML deployment", "intent": "support", "reasoning": "Primary issue is password reset (web) blocking urgent work"}

Example 2:
Input: "We're a Fortune 500 company evaluating vendors for our Q2 AI roadmap"
Output: {"department": "ai", "priority": "high", "summary": "Enterprise AI vendor evaluation", "intent": "sales", "reasoning": "Fortune 500 = VIP sales opportunity for AI services"}

Example 3:
Input: "Can you write a blog post about SEO?"
Output: {"department": "content", "priority": "low", "summary": "SEO blog request", "intent": "sales", "reasoning": "Service request for content team, no urgency"}

Example 4:
Input: "Oh great, another 500 error on Friday night 🙄"
Output: {"department": "web", "priority": "high", "summary": "Recurring 500 errors", "intent": "complaint", "reasoning": "Sarcasm indicates frustration, recurring issue = high priority"}"""

        try:
            client = cls.get_client()
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Updated model (Jan 2025)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Customer Message: {message}"}
                ],
                temperature=0.1,  # Low temperature for consistent classification
                max_tokens=200,
                response_format={"type": "json_object"}  # Force JSON output
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Log classification for debugging
            print(f"🤖 LLM Classification: {message[:50]}... -> {result['department']} ({result['priority']})")
            
            return {
                "summary": result.get("summary", message[:60]),
                "department": result.get("department", "general"),
                "priority": result.get("priority", "medium"),
                "intent": result.get("intent", "inquiry"),
                "reasoning": result.get("reasoning", ""),
                "technical_details": [
                    f"Dept: {result.get('department', 'N/A').upper()}",
                    f"Priority: {result.get('priority', 'N/A').upper()}",
                    f"Intent: {result.get('intent', 'N/A')}",
                    f"Reasoning: {result.get('reasoning', 'N/A')}"
                ]
            }
            
        except Exception as e:
            print(f"❌ LLM Error: {str(e)}")
            # Fallback to basic classification if LLM fails
            return {
                "summary": f"Error classifying: {message[:50]}...",
                "department": "general",
                "priority": "medium",
                "intent": "inquiry",
                "reasoning": f"LLM service error: {str(e)}",
                "technical_details": [
                    "LLM classification failed",
                    "Using fallback classification",
                    f"Error: {str(e)[:100]}"
                ]
            }
