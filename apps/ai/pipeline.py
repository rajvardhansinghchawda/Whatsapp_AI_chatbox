import json
import logging
from apps.ai.api_client import search_hospitals, get_bed_availability
from app.ai_agent import ai_agent

logger = logging.getLogger(__name__)


def process_user_query(user_message: str, phone_number: str) -> str:
    """
    Zero-Hallucination Pipeline:
    1. Detect city + intent via Groq
    2. Fetch real hospital data from public API
    3. Optionally fetch bed availability
    4. Inject data into Groq system prompt
    5. Generate grounded response
    """
    logger.info(f"USER MESSAGE | {phone_number}: {user_message}")

    # 1. Detection Phase — Use Groq to extract metadata
    metadata = _detect_metadata(user_message, phone_number)
    city = metadata.get("city", "")
    intent = metadata.get("intent", "general")
    language = metadata.get("language", "english")

    logger.info(f"DETECTED | city={city} | intent={intent} | language={language}")

    # 2. Data Retrieval Phase
    hospital_context = ""

    if city:
        hospitals = search_hospitals(city=city)

        if hospitals:
            # Build a clean summary for Groq (limit to 6)
            hospital_summaries = []
            for h in hospitals[:6]:
                summary = {
                    "name": h.get("name", "Unknown"),
                    "address": h.get("address", ""),
                    "city": h.get("city", ""),
                    "phone": h.get("phone", ""),
                    "email": h.get("email", ""),
                    "category": h.get("category", ""),
                    "status": h.get("verification_status", ""),
                }

                # If user asks about beds/ICU, fetch bed data too
                if intent in ("beds", "icu", "availability", "emergency"):
                    bed_data = get_bed_availability(h["id"])
                    if bed_data:
                        summary["total_beds"] = bed_data.get("total_beds", 0)
                        summary["available_beds"] = bed_data.get("available_beds", 0)
                        summary["occupied_beds"] = bed_data.get("occupied_beds", 0)
                        if bed_data.get("by_type"):
                            summary["bed_types"] = bed_data["by_type"]

                # Add services if available
                services = h.get("services", [])
                if services:
                    summary["services"] = [s.get("name", "") for s in services[:5]]

                # Add departments if available
                departments = h.get("departments", [])
                if departments:
                    summary["departments"] = [d.get("name", "") for d in departments[:5]]

                hospital_summaries.append(summary)

            hospital_context = f"LIVE HOSPITAL DATA FOR {city.upper()}:\n{json.dumps(hospital_summaries, indent=2)}"
        else:
            hospital_context = (
                f"SYSTEM NOTE: No hospitals found for city '{city}'. "
                "Inform the user naturally. Do NOT invent data. "
                "Suggest trying another city or checking the spelling."
            )
    else:
        hospital_context = (
            "SYSTEM NOTE: User did not mention a specific city. "
            "Ask which city they need hospital information for."
        )

    # 3. Generation Phase
    logger.info("GROQ CALL | Generating grounded response...")
    response = ai_agent.get_response(user_message, phone_number, system_context=hospital_context)

    logger.info(f"FINAL RESPONSE | {phone_number}: {response}")
    return response


def _detect_metadata(user_message: str, phone_number: str) -> dict:
    """
    Use a quick Groq call to detect city, intent, and language from the user message.
    """
    detection_prompt = (
        "You are a metadata extractor. Given a user message, extract:\n"
        "1. city: the city name mentioned (empty string if none)\n"
        "2. intent: one of [hospitals, beds, icu, emergency, ambulance, doctor, appointment, services, general]\n"
        "3. language: detected language [english, hindi, hinglish]\n\n"
        "Respond ONLY in valid JSON. Example: {\"city\": \"Indore\", \"intent\": \"beds\", \"language\": \"hinglish\"}\n\n"
        f"User message: {user_message}"
    )

    try:
        from groq import Groq
        from app.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": detection_prompt}],
            temperature=0,
            max_tokens=100,
        )

        raw = completion.choices[0].message.content.strip()
        logger.info(f"METADATA RAW | {raw}")

        # Parse JSON from response
        # Handle cases where model wraps in markdown
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        return json.loads(raw)
    except Exception as e:
        logger.error(f"METADATA DETECTION ERROR | {e}")
        return {"city": "", "intent": "general", "language": "english"}
