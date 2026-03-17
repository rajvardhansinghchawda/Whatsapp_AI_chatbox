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

    def get_response(self, user_message: str, phone_number: str, system_context: str = "") -> str:
        """
        Sends the user message to Groq and manages chat history for each phone number.
        Incorporates optional system_context for grounded data (API results).
        """
        logger.info(f"Processing message with Groq for {phone_number}: {user_message}")
        
        # Get or create chat history for this phone number
        if phone_number not in self.chat_sessions:
            logger.info(f"Creating new chat session for {phone_number}")
            self.chat_sessions[phone_number] = [
                {"role": "system", "content": settings.SYSTEM_PROMPT}
            ]

        # Update system prompt with fresh context if provided
        # We always keep the first message as the system entry, but we can update its content
        final_system_prompt = settings.SYSTEM_PROMPT
        if system_context:
            final_system_prompt = f"{settings.SYSTEM_PROMPT}\n\n### LIVE DATA CONTEXT ###\n{system_context}\n\nSTRICT RULE: Use ONLY this data for hospital queries. Never invent names or counts."
        
        self.chat_sessions[phone_number][0]["content"] = final_system_prompt

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
            
            # Post-processing to remove any self-identification as "Groq" or "Llama"
            if "i am llama" in response_text.lower() or "i am groq" in response_text.lower():
                logger.warning(f"Persona leak detected for {phone_number}. Cleaning response.")
                response_text = response_text.replace("I am Llama", "I am your hospital assistant")
                response_text = response_text.replace("I am Groq", "I am your hospital assistant")

            # Add assistant response to history
            self.chat_sessions[phone_number].append({"role": "assistant", "content": response_text})
            
            # Limit history size (keep last 10 exchanges + system prompt)
            if len(self.chat_sessions[phone_number]) > 21:
                self.chat_sessions[phone_number] = [self.chat_sessions[phone_number][0]] + self.chat_sessions[phone_number][-20:]

            return response_text.strip()
            
        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Groq API Error ({type(e).__name__}) for {phone_number}: {str(e)}")
            
            if "rate_limit" in error_msg or "429" in error_msg:
                return "The hospital AI service is very busy right now. Please wait a moment and try again."
            
            if "context_length" in error_msg:
                logger.warning(f"Context length exceeded for {phone_number}. Clearing history.")
                self.chat_sessions[phone_number] = [self.chat_sessions[phone_number][0]] # Keep system prompt
                return "Your conversation was getting a bit long! I've cleared the history to keep our chat smooth. How can I help you further?"

            return "I'm having a bit of trouble processing your hospital query. Please try again soon."

ai_agent = AIAgent()
