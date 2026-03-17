from groq import Groq
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"
            self.chat_sessions = {}  # Dictionary to store message history: {phone_number: list[dict]}
            logger.info(f"Groq AIAgent initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq AIAgent: {e}", exc_info=True)

    def get_response(self, user_message: str, phone_number: str) -> str:
        """
        Sends the user message to Groq and manages chat history for each phone number.
        """
        logger.info(f"Processing message with Groq for {phone_number}: {user_message}")
        
        # Get or create chat history for this phone number
        if phone_number not in self.chat_sessions:
            logger.info(f"Creating new chat session for {phone_number}")
            self.chat_sessions[phone_number] = [
                {"role": "system", "content": settings.SYSTEM_PROMPT}
            ]

        # Add user message to history
        self.chat_sessions[phone_number].append({"role": "user", "content": user_message})

        try:
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_sessions[phone_number],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            response_text = completion.choices[0].message.content
            
            # Add assistant response to history
            self.chat_sessions[phone_number].append({"role": "assistant", "content": response_text})
            
            # Limit history size to prevent context overflow (e.g., keep last 10 exchanges + system prompt)
            if len(self.chat_sessions[phone_number]) > 21:
                self.chat_sessions[phone_number] = [self.chat_sessions[phone_number][0]] + self.chat_sessions[phone_number][-20:]

            return response_text.strip()
            
        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Groq API Error ({error_type}) for {phone_number}: {str(e)}")
            
            if "rate_limit_exceeded" in str(e).lower() or "429" in str(e):
                return "The AI service is currently busy (Rate limit reached). Please wait a minute and try again."
            
            return f"Error: {error_type}. I'm having trouble processing your request. Please try again later."

ai_agent = AIAgent()
