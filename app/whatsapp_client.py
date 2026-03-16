import logging
import requests
from app.config import settings

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.PHONE_NUMBER_ID
        self.api_version = settings.WHATSAPP_API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def send_text_message(self, to_phone_number: str, message_body: str):
        """
        Sends a text message to a user via the WhatsApp Cloud API.
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "text",
            "text": {
                "body": message_body
            }
        }
        
        try:
            logger.info(f"Sending WhatsApp message to {to_phone_number}")
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"WhatsApp message sent successfully to {to_phone_number}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error sending WhatsApp message: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return None

whatsapp_client = WhatsAppClient()
