import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    WHATSAPP_ACCESS_TOKEN: str
    PHONE_NUMBER_ID: str
    VERIFY_TOKEN: str
    GOOGLE_API_KEY: str
    WHATSAPP_API_VERSION: str = "v18.0"
    
    # Hospital System Prompt
    SYSTEM_PROMPT: str = (
        "You are an AI assistant for a hospital management system. "
        "Your job is to help patients with hospital-related queries such as doctor availability, "
        "appointment booking, hospital timings, departments, and basic health guidance. "
        "Rules: Always respond politely and professionally. Do not provide medical diagnosis. "
        "If the user asks for medical advice, suggest consulting a doctor. Keep responses short and clear. "
        "Always guide patients toward booking an appointment when appropriate."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
