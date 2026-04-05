import os
import requests
import logging
from typing import Dict

# Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PinakBrain")

class PinakBrain:
    """
    ULTIMATE 2026 HYBRID EDITION - Project Pinak Core Brain.
    Fix: Combines elite sanitization from old code with environment-first logic of new code.
    """

    def __init__(self, config_path: str = "secure_keys/config.txt"):
        self.config_path = config_path
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # 2026 ELITE MODELS: Llama 3.3 is the primary beast
        self.model_stack = [
            "llama-3.3-70b-versatile", 
            "llama-3.1-70b-versatile", 
            "llama3-70b-8192"
        ]
        self.api_key = self._initialize_brain()

    def _initialize_brain(self) -> str:
        """Military-Grade Key Ingestion: Direct Environment Check then Local Fallback."""
        # PRIORITY 1: Cloud/Render Env Var
        env_key = os.getenv("GROQ_API_KEY")
        if env_key:
            logger.info("Cloud Environment detected. Injecting Secure Key...")
            return self._sanitize_key(env_key)

        # PRIORITY 2: Local File for Laptop Dev
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
        """Professional byte-level cleaning to prevent API handshake errors."""
        clean_key = "".join(c for c in key if c.isprintable() and not c.isspace())
        return clean_key.replace('"', '').replace("'", "")

    def generate_response(self, user_prompt: str) -> str:
        if not self.api_key:
            return "FATAL_ERROR: API_KEY_MISSING. Check Render Env Vars or Local config.txt"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Elite Model-Stack Fallback Loop
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
                
                logger.warning(f"Model {current_model} failed (Status: {response.status_code}). Trying next...")
            except Exception as e:
                logger.error(f"Network error on {current_model}: {e}")
        
        return "STALEMATE: All models failed. Check your API quota or Network."

if __name__ == "__main__":
    print("--- Project Pinak: Elite 2026 Brain Node ---")
    pinak = PinakBrain()
    print("Initiating Secure Connection Stack...")
    print(f"\n[PINAK_OUTPUT]: {pinak.generate_response('Confirm system operational status.')}")