import logging
import json
from apps.ai.api_client import get_hospitals
from app.ai_agent import ai_agent

logger = logging.getLogger(__name__)

def process_user_query(user_text: str, phone_number: str) -> str:
    """
    Full AI Processing Pipeline:
    User message -> Language/City/Intent Detect -> API Call -> Grounded Groq Response.
    """
    logger.info(f"USER MESSAGE | {phone_number}: {user_text}")

    # 1. Detection Phase
    detection = _detect_metadata(user_text)
    city = detection.get("city")
    intent = detection.get("intent")
    language = detection.get("language")
    
    logger.info(f"DETECTED | City: {city} | Intent: {intent} | Lang: {language}")

    # 2. Retrieval Phase
    hospital_context = ""
    if city:
        data = get_hospitals(city)
        if data and data.get("hospitals"):
            hospitals = data.get("hospitals")[:6]
            hospital_context = f"LIVE HOSPITAL DATA:\n{json.dumps(hospitals, indent=2)}"
        else:
            hospital_context = "SYSTEM: No hospitals found in this city."

    # 3. Generation Phase
    logger.info("GROQ CALL | Generating grounded response...")
    response = ai_agent.get_response(user_text, phone_number, system_context=hospital_context)
    
    # 4. Final Polish
    # Append follow-up if not present
    if "?" not in response:
        response += " How else can I help you today?"

    logger.info(f"FINAL RESPONSE | {response}")
    return response

def _detect_metadata(text: str) -> dict:
    """Detects city, intent, and language using a single Llama 3.1 call."""
    prompt = f"""
    Analyze query: "{text}"
    Extract JSON with:
    - city: Name if mentioned, else null.
    - intent: [hospital_search, bed_availability, symptoms, sms_request, general].
    - language: [Hindi, English, Mixed].
    """
    try:
        res = ai_agent.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(res.choices[0].message.content)
    except Exception:
        return {"city": None, "intent": "general", "language": "English"}
