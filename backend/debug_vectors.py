from app.services.vector_service import VectorService

def debug():
    print("Initializing Model...")
    VectorService.get_model()
    
    queries = [
        "Where is your office located?",
        "I want my money back",
        "My server is down 500",
        "Train a new model"
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        result = VectorService.search(q, threshold=0.0) # Get all matches
        if result:
            print(f"Match: {result['doc']['text'][:50]}...")
            print(f"Score: {result['score']}")
        else:
            print("No match found.")

if __name__ == "__main__":
    debug()
