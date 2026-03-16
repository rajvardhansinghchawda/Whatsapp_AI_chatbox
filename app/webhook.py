import logging
from fastapi import APIRouter, Request, Query, HTTPException, Response
from app.config import settings
from app.ai_agent import ai_agent
from app.whatsapp_client import whatsapp_client

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    """
    WhatsApp Webhook verification for Meta Developer Platform.
    """
    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        logger.info("Webhook verified successfully.")
        return Response(content=challenge, media_type="text/plain")
    
    logger.warning("Webhook verification failed.")
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/webhook")
async def handle_whatsapp_message(request: Request):
    """
    Receives incoming WhatsApp messages, processes them with AI, and sends back a response.
    """
    data = await request.json()
    import json
    logger.info(f"Full Webhook Data: {json.dumps(data, indent=2)}")

    try:
        # WhatsApp payload structure is deeply nested
        # See: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value.get("messages", []):
                            phone_number = message.get("from")
                            message_text = message.get("text", {}).get("body")

                            if phone_number and message_text:
                                logger.info(f"Processing message from {phone_number}: {message_text}")
                                
                                # 1. Generate AI Response with context (phone_number)
                                ai_response = ai_agent.get_response(message_text, phone_number)
                                
                                # 2. Send response back via WhatsApp
                                whatsapp_client.send_text_message(phone_number, ai_response)
                                
                                logger.info(f"Sent AI response to {phone_number}")

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
