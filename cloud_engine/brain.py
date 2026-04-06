import os
import requests
import logging
import time
from typing import Dict

# Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PinakBrain")

class PinakBrain:
    """
    ULTIMATE 2026 PERSISTENT EDITION - Project Pinak Core Brain.
    Fix: Added persistent heartbeat to bypass Render's port-scan/timeout errors.
    """

    def __init__(self, config_path: str = "secure_keys/config.txt"):
        self.config_path = config_path
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # 2026 ELITE MODELS
        self.model_stack = [
            "llama-3.3-70b-versatile", 
            "llama-3.1-70b-versatile", 
            "llama3-70b-8192"
        ]
        self.api_key = self._initialize_brain()

    def _initialize_brain(self) -> str:
        """Key Ingestion with Cloud-First Logic."""
        env_key = os.getenv("GROQ_API_KEY")
        if env_key:
            logger.info("Cloud Environment detected. Injecting Secure Key...")
            return self._sanitize_key(env_key)

        if os.path.exists(self.config_path):
            logger.info("Local environment detected. Loading config file...")
            try:
                encodings = ['utf-8-sig', 'utf-16', 'utf-8']
                for enc in encodings:
                    with open(self.config_path, "r", encoding=enc) as f:
                        content = f.read()
                        if "=" in content:
                            raw_key = content.split("=")[1].strip()
                            return self._sanitize_key(raw_key)
            except Exception as e:
                logger.error(f"Local file read error: {e}")
        
        return ""

    def _sanitize_key(self, key: str) -> str:
        """Removes quotes, spaces, and non-printable characters."""
        clean_key = "".join(c for c in key if c.isprintable() and not c.isspace())
        return clean_key.replace('"', '').replace("'", "")

    def generate_response(self, user_prompt: str) -> str:
        if not self.api_key:
            return "FATAL_ERROR: API_KEY_MISSING. Check Render Env Vars."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for current_model in self.model_stack:
            payload = {
                "model": current_model,
                "messages": [
                    {"role": "system", "content": "You are Pinak, an elite 2026 AI agent. Be technical and precise."},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.5
            }

            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                
                logger.warning(f"Model {current_model} failed (Status: {response.status_code}).")
            except Exception as e:
                logger.error(f"Network error on {current_model}: {e}")
        
        return "STALEMATE: All models failed."

if __name__ == "__main__":
    print("--- Project Pinak: Elite 2026 Brain Node ---")
    pinak = PinakBrain()
    
    # Initial Handshake Check
    logger.info("Initiating Secure Connection Stack...")
    handshake = pinak.generate_response("System check: Confirm operational status.")
    print(f"\n[PINAK_OUTPUT]: {handshake}")

    # PERSISTENCE LOOP (The Port Fix)
  
    logger.info("Entering Standing Mode. System is now 24/7 Persistent.")
    try:
        while True:
          
            logger.info("Heartbeat: Pinak Node is active and monitoring.")
            time.sleep(600) 
    except KeyboardInterrupt:
        logger.info("System shutting down gracefully.")