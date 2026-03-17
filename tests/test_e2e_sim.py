import os
import sys
# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
import json
from unittest.mock import patch
import os

client = TestClient(app)

def test_webhook_e2e_simulation():
    # Mock payload from WhatsApp
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15555555555",
                                "phone_number_id": "123456789"
                            },
                            "messages": [
                                {
                                    "from": "911234567890",
                                    "id": "mid.123",
                                    "timestamp": "123456789",
                                    "text": {
                                        "body": "Hello, I need to book an appointment."
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

    print("\n[Simulating Webhook Request]")
    
    # Mock the whatsapp_client.send_text_message to avoid actual API calls
    with patch("app.webhook.whatsapp_client.send_text_message") as mock_send:
        response = client.post("/webhook", json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        
        # Verify that send_text_message was called
        assert mock_send.called
        args, kwargs = mock_send.call_args
        phone_number, response_text = args
        
        print(f"Verified send_text_message called for: {phone_number}")
        print(f"AI Response Snippet: {response_text[:50]}...")
        
        # Verify persona keywords in response
        response_lower = response_text.lower()
        assert "hospital" in response_lower or "doctor" in response_lower or "help" in response_lower or "appointment" in response_lower

    print("[SUCCESS] E2E Simulation passed.")

if __name__ == "__main__":
    test_webhook_e2e_simulation()
