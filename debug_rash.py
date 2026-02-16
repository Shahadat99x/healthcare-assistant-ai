import sys
import os

# Adjust path to import from apps/api
sys.path.append(os.path.join(os.getcwd(), 'apps', 'api'))

from services.rag_service import rag_service

def debug_rash():
    rag_service.initialize()
    query = "Rash for 2 weeks"
    print(f"Query: {query}")
    
    # We need to manually simulate what retrieve does before filtering
    # But rag_service.retrieve now HAS the filter.
    # So let's just call it and see if it returns anything.
    
    results = rag_service.retrieve(query, symptom_tags=["rash"], k=5)
    print(f"Results count: {len(results)}")
    for r in results:
        print(f" - {r['title']} ({r['org']})")
        print(f"   Snippet: {r['snippet']}")

if __name__ == "__main__":
    debug_rash()
