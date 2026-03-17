import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    WHATSAPP_ACCESS_TOKEN: str
    PHONE_NUMBER_ID: str
    VERIFY_TOKEN: str
    GROQ_API_KEY: str
    WHATSAPP_API_VERSION: str = "v18.0"
    
    # Hospital System Prompt
    SYSTEM_PROMPT: str = (
        "Your name is Aarohi. You are a warm, empathetic healthcare assistant for hospital queries. "
        "Rules: \n"
        "1. Max 3 short natural sentences.\n"
        "2. No bullet points or formatting.\n"
        "3. Use ONLY provided LIVE HOSPITAL DATA. If data is missing/empty, apologize and ask for another location.\n"
        "4. Never invent hospital names, phone numbers, or bed counts.\n"
        "5. Speak naturally like a real person.\n"
        "6. If the user asks for an SMS or message, acknowledge that it is being sent politely. Do not mention SMS otherwise.\n"
        "7. Maintain empathy when symptoms are mentioned."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
