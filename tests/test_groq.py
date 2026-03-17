import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ai_agent import AIAgent
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_groq_integration():
    print("Initializing Groq AI Agent...")
    agent = AIAgent()
    
    test_phone = "1234567890"
    test_message = "Hello, what services do you provide?"
    
    print(f"Sending message: {test_message}")
    response = agent.get_response(test_message, test_phone)
    
    print("\n--- Groq Response ---")
    print(response)
    print("----------------------\n")
    
    if response and "hospital" in response.lower() or "doctor" in response.lower() or "help" in response.lower():
        print("SUCCESS: Response seems relevant to the hospital system prompt.")
    else:
        print("WARNING: Response might not be following the system prompt strictly, or Groq is returned an error.")

if __name__ == "__main__":
    test_groq_integration()
