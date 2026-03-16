import logging
from fastapi import FastAPI
from app.webhook import router as webhook_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI(title="WhatsApp Hospital Bot")

@app.get("/")
async def root():
    return {"message": "WhatsApp Hospital AI Bot is running."}

# Include routers
app.include_router(webhook_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
