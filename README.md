# WhatsApp Hospital AI Bot

A senior-level WhatsApp AI chatbot system integrated with Meta's WhatsApp Cloud API for a Hospital Management System (HMS).

## Features
- **Stateful Memory**: Remembers past conversations for each user based on their phone number.
- **Webhook Handling**: Secure verification and processing of incoming WhatsApp messages.
- **AI Integration**: Powered by Google's Gemini API (`gemini-flash-latest`) with specialized hospital system prompt and safety overrides.
- **WhatsApp Client**: Robust client for sending responses via Meta Graph API.
- **Modern Stack**: Built with FastAPI for high performance.

## Project Structure
```text
whatsapp_hospital_bot/
│
├── app/
│   ├── main.py           # Entry point
│   ├── webhook.py        # Webhook handler
│   ├── ai_agent.py       # AI interaction layer
│   ├── whatsapp_client.py # WhatsApp API client
│   ├── config.py         # Configuration management
│
├── .env                  # Secrets (gitignored)
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your credentials from Meta Developer Console and Google.
   ```bash
   WHATSAPP_ACCESS_TOKEN=...
   PHONE_NUMBER_ID=...
   VERIFY_TOKEN=...
   GOOGLE_API_KEY=...
   ```

3. **Run the Application**:
   ```bash
   python -m app.main
   ```
   The server will start on `http://localhost:8000`.

4. **Expose Local Server**:
   Use `ngrok` to expose your local port 8000 to the internet for Meta's Webhook.
   ```bash
   ngrok http 8000
   ```

5. **Configure Meta Webhook**:
   - Go to your app in Facebook Developer Console.
   - Set Webhook URL to `https://your-ngrok-url/webhook`.
   - Set Verify Token to match the one in your `.env`.
   - **Important**: In the Webhooks setup, click "Manage" and subscribe to the `messages` field.

## Memory Implementation
The bot uses Gemini's `ChatSession` to maintain context. History is currently stored in-memory (it will reset if the server restarts).

