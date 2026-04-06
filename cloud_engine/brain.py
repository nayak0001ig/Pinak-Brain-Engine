import os
import requests
import logging
import time
import threading
import uvicorn
from typing import Dict, List
from fastapi import FastAPI

# --- Professional Logging Setup ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PinakBrain")

# --- FastAPI Initialization (Render Health Check Protocol) ---
app = FastAPI(title="Project Pinak: Brain Node", version="2.0.26")

@app.get("/")
async def root():
    """Service Health Check Endpoint."""
    return {
        "status": "ONLINE",
        "node": "Elite 2026 Brain Node",
        "timestamp": time.time()
    }

class PinakBrain:
    """
    ULTIMATE 2026 PERSISTENT EDITION - Project Pinak Core Brain.
    Features: FastAPI Port Binding, Multi-Model Fallback, and Key Sanitization.
    """

    def __init__(self, config_path: str = "secure_keys/config.txt"):
        self.config_path = config_path
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model_stack = [
            "llama-3.3-70b-versatile", 
            "llama-3.1-70b-versatile", 
            "llama3-70b-8192"
        ]
        self.api_key = self._initialize_brain()

    def _initialize_brain(self) -> str:
        """Secure Key Ingestion: Environment Variable Priority with Local Fallback."""
        env_key = os.getenv("GROQ_API_KEY")
        if env_key:
            logger.info("Cloud Environment detected. Injecting Secure Key...")
            return self._sanitize_key(env_key)

        if os.path.exists(self.config_path):
            logger.info("Local environment detected. Loading configuration file...")
            try:
                encodings = ['utf-8-sig', 'utf-16', 'utf-8']
                for enc in encodings:
                    with open(self.config_path, "r", encoding=enc) as f:
                        content = f.read()
                        if "=" in content:
                            raw_key = content.split("=")[1].strip()
                            return self._sanitize_key(raw_key)
            except Exception as e:
                logger.error(f"Configuration ingestion failure: {e}")
        
        return ""

    def _sanitize_key(self, key: str) -> str:
        """Byte-level sanitization to ensure API handshake integrity."""
        clean_key = "".join(c for c in key if c.isprintable() and not c.isspace())
        return clean_key.replace('"', '').replace("'", "")

    def generate_response(self, user_prompt: str) -> str:
        """Executes high-performance inference across the model stack."""
        if not self.api_key:
            return "FATAL_ERROR: API_KEY_MISSING. Check Environment Variables."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for current_model in self.model_stack:
            payload = {
                "model": current_model,
                "messages": [
                    {"role": "system", "content": "You are Pinak, an elite 2026 AI agent. Provide technical and precise responses."},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.5
            }

            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                
                logger.warning(f"Inference failed on {current_model} (Status: {response.status_code}).")
            except Exception as e:
                logger.error(f"Network exception on {current_model}: {e}")
        
        return "STALEMATE: All nodes in the model stack failed to respond."

# --- Singleton Brain Instance ---
pinak_instance = PinakBrain()

def run_system_handshake():
    """Initializes the cognitive engine and performs a system check."""
    logger.info("--- Project Pinak: Elite 2026 Brain Node ---")
    logger.info("Initiating Secure Connection Stack...")
    handshake = pinak_instance.generate_response("Confirm system operational status.")
    logger.info(f"System Handshake Result: {handshake}")
    
    # Persistent Heartbeat Loop
    while True:
        logger.info("Heartbeat: Pinak Node is active and monitoring.")
        time.sleep(600)

if __name__ == "__main__":
    # Start the Brain Engine and Heartbeat in a background thread
    threading.Thread(target=run_system_handshake, daemon=True).start()
    
    # Start the FastAPI Web Server to satisfy Render's Port binding requirement
    # Render's dynamic port is captured via the PORT environment variable
    server_port = int(os.environ.get("PORT", 10000))
    logger.info(f"Exposing Node on port {server_port} for cloud health checks.")
    uvicorn.run(app, host="0.0.0.0", port=server_port)