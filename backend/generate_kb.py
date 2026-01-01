import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Load env for API key (New Key from User)
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# TOPICS: CLIENT PERSONA (Not Developer)
# These are questions a non-technical or semi-technical CLIENT asks a Software House.
TOPICS = {
    "project_management": [
        "Project timeline and delays (when will it be done?)",
        "Change requests and scope creep (can I add a feature?)",
        "Communication channels (slack, email, meetings)",
        "Deliverables and milestones (what do I get?)",
        "User Acceptance Testing (UAT) process",
        "Intellectual Property and code ownership"
    ],
    "web_services": [
        "Domain name registration and renewal",
        "Hosting costs and server ownership",
        "Website maintenance and security updates",
        "Mobile responsiveness and cross-browser testing",
        "CMS training (how do I edit content?)",
        "SEO basics included in development"
    ],
    "ai_solutions": [
        "Data privacy and security (is my data safe?)",
        "AI Model accuracy expectations",
        "Ongoing costs for AI (tokens, GPU servers)",
        "Integration with existing systems",
        "Custom model training vs pre-trained"
    ],
    "commercial": [
        "Payment terms (milestones, upfront, net30)",
        "Retainer agreements for ongoing support",
        "Pricing factors (fixed price vs time & material)",
        "Contract termination clauses",
        "NDA and confidentiality"
    ],
    "support": [
        "Reporting a critical bug (system down)",
        "Response time SLAs (how fast will you fix it?)",
        "Requesting a new feature after launch",
        "Lost access or password recovery for admin panel",
        "Backup and disaster recovery"
    ]
}

def generate_faqs_for_topic(category, topic, count=30):
    """
    Generate CLIENT-FACING FAQs.
    """
    prompt = f"""
    You are writing FAQs for a Software Development Agency's Client Portal.
    Topic: '{topic}'
    Category: {category}
    
    Target Audience: Business clients (not developers). They care about cost, timeline, business value, and support.
    
    Generate {count} realistic questions and answers a CLIENT would ask.
    
    Output MUST be a valid JSON list of objects:
    [
        {{
            "text": "Answer (professional, reassuring, max 2 sentences).",
            "question_variant": "The question the client asked (e.g. 'Can I change my logo?')",
            "category": "{category}",
            "subcategory": "slug",
            "intent": "inquiry|support|complaint",
            "keywords": ["keyword1", "keyword2"]
        }}
    ]
    
    Note: In the 'text' field, include the Answer, but frame it so it stands alone or repeats the context.
    Example Text: "Yes, we providing logo edits during the design phase. Additional changes may incur a fee."
    
    RETURN ONLY JSON.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        content = completion.choices[0].message.content
        data = json.loads(content)
        if isinstance(data, dict):
            # Try to find list in values
            for v in data.values():
                if isinstance(v, list): return v
            return []
        return data
        
    except Exception as e:
        print(f"❌ Error generating {topic}: {e}")
        return []

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.join(base_dir, 'app', 'core', 'knowledge_base.json')
    
    # Load existing (The Seed Data)
    current_kb = []
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            current_kb = json.load(f)
    
    next_id = max([item.get('id', 0) for item in current_kb], default=0) + 1
    total_new = 0
    
    print("🚀 Starting Customer-Centric FAQ Generation...")
    
    for category, topics in TOPICS.items():
        print(f"\n📂 Processing: {category.upper()}")
        for topic in topics:
            print(f"   Generating ~30 FAQs for: {topic}...")
            
            new_faqs = generate_faqs_for_topic(category, topic, count=30)
            
            for faq in new_faqs:
                faq['id'] = next_id
                next_id += 1
                # Format text to include question context if needed, but RAG usually searches against 'text'.
                # To make RAG better, let's combine Question + Answer in 'text' or keep them separate?
                # Current system searches 'text'. Let's Ensure 'text' is the ANSWER, but rich in keywords.
                # Actually, standard RAG chunks usually contain the Answer. The query matches the answer's meaning.
                # But sometimes matching Q to Q is better. 
                # Let's stick to Text = Answer, but make sure Answer is descriptive.
                
                current_kb.append(faq)
                total_new += 1
            
            print(f"   ✅ Added {len(new_faqs)} FAQs. Total: {len(current_kb)}")
            
            with open(kb_path, 'w', encoding='utf-8') as f:
                json.dump(current_kb, f, indent=2)
                
            time.sleep(2) # Be polite to new key
            
    print(f"\n🎉 Generation Complete! Total Knowledge Base: {len(current_kb)}")

if __name__ == "__main__":
    main()
