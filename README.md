# 🏥 Aarohi: WhatsApp Hospital AI Bot

Aarohi is a premium WhatsApp AI chatbot designed for real-time Healthcare Resource Coordination. Integrated with **Meta's WhatsApp Cloud API** and powered by **Groq (Llama 3.1)**, it helps patients and caregivers find ICU beds, doctors, and emergency services across multiple hospitals.

---

## ✨ Key Features

- **🧠 Stateful Memory**: Maintains conversation context for each user based on their phone number.
- **📍 Location Intelligence**: Processes both text-based locations and **WhatsApp Location Pins** for nearby hospital discovery.
- **🚑 Emergency Protocol**: Detects critical symptoms (e.g., chest pain, accidents) and prioritizes immediate hospital/ambulance routing.
- **💉 Real-time Data**: Integrated with a live hospital management backend for up-to-date bed availability (ICU, Ventilator, General).
- **🗣️ Multi-lingual Support**: Handles English, Hindi, and Hinglish for natural patient interaction.
- **🔒 Zero-Hallucination Pipeline**: Uses a strict grounded-data approach to ensure hospital names and counts are never invented.

---

## 🛠️ Modern Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python web framework)
- **AI Engine**: [Groq](https://groq.com/) (Llama-3.1-8b-instant) for lightning-fast inference.
- **Messaging**: [Meta WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/) & Pydantic Settings

---

## 📂 Project Structure

```text
chatbox/
├── app/                  # FastAPI Application Core
│   ├── main.py           # Application Entry Point
│   ├── webhook.py        # WhatsApp Webhook & Event Handlers
│   ├── ai_agent.py       # Groq AI Orchestration
│   ├── whatsapp_client.py # Meta Graph API Integration
│   └── config.py         # System Prompts & Configuration
├── apps/                 # Modular Business Logic
│   └── ai/
│       ├── api_client.py # Hospital Backend API Client
│       └── pipeline.py   # Detection & Grounding Pipeline
├── scripts/              # Utility & Automation Scripts
├── tests/                # Unit & Integration Tests
├── .env                  # Environment Secrets
├── requirements.txt      # Python Dependencies
└── README.md             # Project Documentation
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Meta Developer Account (WhatsApp Cloud API access)
- Groq API Key

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd chatbox

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
WHATSAPP_ACCESS_TOKEN=your_meta_token
PHONE_NUMBER_ID=your_phone_id
VERIFY_TOKEN=your_custom_verify_token
GROQ_API_KEY=your_groq_key
```

### 4. Running the Bot
```bash
# Start the FastAPI server
python -m app.main
```
The server defaults to `http://localhost:8000`.

### 5. Webhook Integration
1. Use **ngrok** to expose your local port: `ngrok http 8000`.
2. Update the Webhook URL in Meta's Dashboard to `https://<ngrok-id>.ngrok-free.app/webhook`.
3. Subscribe to **messages** in the Webhooks settings.

---

## 🤖 Persona: Aarohi
Aarohi is designed to be **empathetic, calm, and accurate**. She follows a strict interaction style:
- Clear, simple conversational language.
- Maximum 3 short sentences per response.
- No bullet points or markdown in messages (optimized for WhatsApp).
- Directs users to verified resources only.

---

## ⚠️ Limitations
- **History Storage**: Currently uses in-memory storage (clears on server restart).
- **Rate Limits**: Subject to Groq and Meta Cloud API usage tiers.

---

## 🛡️ License & Disclaimer
*This project is for Healthcare Resource Coordination. Always consult medical professionals for clinical advice.*
