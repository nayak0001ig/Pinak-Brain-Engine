import os
import requests
import logging
import time
import threading
import uvicorn
from typing import Dict
from fastapi import FastAPI, Header, HTTPException, Request

# --- Professional Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PinakBrain")

# --- FastAPI Initialization ---
app = FastAPI(title="Project Pinak: Elite Receiver", version="2.1.0")

# SECURITY: Internal Handshake Key (Fetch from Render Env)
# Default value is a backup, but always set this in Render Dashboard for "Tight Security"
INTERNAL_AUTH_KEY = os.getenv("INTERNAL_SECRET_KEY", "Pinak_Secure_2026_v1")

class PinakBrain:
    def __init__(self, config_path: str = "secure_keys/config.txt"):
        self.config_path = config_path
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model_stack = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]
        self.api_key = self._initialize_brain()

    def _initialize_brain(self) -> str:
        env_key = os.getenv("GROQ_API_KEY")
        if env_key: return self._sanitize_key(env_key)
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                content = f.read()
                if "=" in content: return self._sanitize_key(content.split("=")[1])
        return ""

    def _sanitize_key(self, key: str) -> str:
        return "".join(c for c in key if c.isprintable() and not c.isspace()).replace('"', '').replace("'", "")

    def generate_response(self, user_prompt: str) -> str:
        if not self.api_key: return "FATAL_ERROR: API_KEY_MISSING."
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model_stack[0],
            "messages": [
                {"role": "system", "content": "You are Pinak, an elite 2026 AI agent for the brand NAYRIT. Be technical and precise."},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.5
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error Code: {response.status_code}"
        except Exception as e:
            return f"Network Exception: {str(e)}"

# Singleton Instance
pinak_instance = PinakBrain()

# --- WEBHOOK ENDPOINT: This is where WhatsApp will send messages ---
@app.post("/chat")
async def chat_receiver(request: Request, x_api_key: str = Header(None)):
    """
    TIGHT SECURITY: Only authorized gateways can talk to the brain.
    """
    if x_api_key != INTERNAL_AUTH_KEY:
        logger.warning(f"Unauthorized access attempt blocked from IP: {request.client.host}")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message:
            return {"status": "error", "reply": "No message received."}

        logger.info(f"Processing message for NAYRIT: {user_message[:20]}...")
        ai_reply = pinak_instance.generate_response(user_message)
        
        return {"status": "success", "reply": ai_reply}
    except Exception as e:
        logger.error(f"Endpoint Error: {e}")
        return {"status": "error", "reply": "System processing failure."}

@app.get("/")
async def health():
    return {"status": "ONLINE", "mode": "Secure Receiver Active"}

# --- Background Heartbeat ---
def run_heartbeat():
    while True:
        logger.info("Heartbeat: Pinak Secure Node is monitoring traffic.")
        time.sleep(600)

if __name__ == "__main__":
    threading.Thread(target=run_heartbeat, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Pinak Elite Node exposing on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)