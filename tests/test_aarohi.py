import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.ai.pipeline import process_user_query
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_aarohi_pipeline():
    print("\n[Testing Aarohi Pipeline - Zero Hallucination]")
    
    test_queries = [
        "Indore me ICU availability dikhao",
        "Hello, my head hurts. Are there any hospitals in Bhopal?",
        "Sms bhejo details ka"
    ]
    
    phone = "919876543210"
    
    for query in test_queries:
        print(f"\nQUERY: {query}")
        response = process_user_query(query, phone)
        print(f"AAROHI: {response}")
        
        # Basic validation
        if len(response.split('.')) > 5:
            print("WARNING: Response seems too long (> 3-4 sentences).")
        if "Aarohi" in response:
            print("Persona check: Aarohi mentioned herself.")

if __name__ == "__main__":
    test_aarohi_pipeline()
