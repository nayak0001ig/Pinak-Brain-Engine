import os
import requests
import logging
import time
import threading
import uvicorn
from fastapi import FastAPI

# Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PinakBrain")

# FastAPI Initialization to satisfy Render's Port Binding
app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ONLINE", "node": "Pinak Elite 2026"}

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
        if not self.api_key: return "API_KEY_MISSING"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model_stack[0],
            "messages": [{"role": "user", "content": user_prompt}]
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
            return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "ERROR"
        except: return "NETWORK_ERROR"

# --- Main Logic ---
pinak = PinakBrain()

def run_heartbeat():
    logger.info("--- Project Pinak: Elite 2026 Brain Node ---")
    logger.info(f"Handshake: {pinak.generate_response('Confirm status.')}")
    while True:
        logger.info("Heartbeat: Pinak Node is active and monitoring.")
        time.sleep(600)

if __name__ == "__main__":
    # Start Heartbeat in background
    threading.Thread(target=run_heartbeat, daemon=True).start()
    
    # Start Web Server for Render
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Binding to port {port} for Render Health Check.")
    uvicorn.run(app, host="0.0.0.0", port=port)