import google.generativeai as genai
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            
            # Define safety settings to be less restrictive
            # Using the exact category names required by the API
            self.safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            self.model = genai.GenerativeModel(
                'gemini-flash-latest', 
                system_instruction=settings.SYSTEM_PROMPT,
                safety_settings=self.safety_settings
            )
            self.chat_sessions = {}  # Dictionary to store sessions: {phone_number: ChatSession}
            logger.info("Gemini AIAgent initialized with safety overrides.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AIAgent: {e}", exc_info=True)

    def get_response(self, user_message: str, phone_number: str) -> str:
        """
        Sends the user message to the user's specific Gemini ChatSession.
        """
        logger.info(f"Processing message with Gemini for {phone_number}: {user_message}")
        
        # Get or create chat session for this phone number
        if phone_number not in self.chat_sessions:
            logger.info(f"Creating new chat session for {phone_number}")
            # Ensure safety_settings are also passed to start_chat if needed
            self.chat_sessions[phone_number] = self.model.start_chat(history=[])

        try:
            chat = self.chat_sessions[phone_number]
            # Some SDK versions prefer safety_settings passed here
            response = chat.send_message(user_message, safety_settings=self.safety_settings)
            
            try:
                if response.text:
                    return response.text.strip()
            except ValueError:
                # This usually happens when the response is blocked
                if response.prompt_feedback:
                    logger.warning(f"Gemini prompt blocked for {phone_number}: {response.prompt_feedback}")
                elif response.candidates:
                    logger.warning(f"Gemini candidate blocked for {phone_number}: {response.candidates[0].finish_reason}")
                return "I'm sorry, I cannot respond to that message due to safety filters. Please try asking differently."
                
            return "I'm sorry, I couldn't generate a response."
        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Gemini API Error ({error_type}) for {phone_number}: {str(e)}")
            
            if "429" in str(e) or "ResourceExhausted" in error_type:
                return "The AI service is currently busy (Quota limit reached). Please wait a minute and try again."
            
            return f"Error: {error_type}. I'm having trouble processing your request. Please try again later."

ai_agent = AIAgent()
