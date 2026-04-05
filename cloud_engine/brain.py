import os
import requests
import json
import logging
from typing import Optional, Dict, List, Any

# Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PinakBrain")

class PinakBrain:
    """
    ULTIMATE 2026 HYBRID EDITION - Project Pinak Core Brain.
    Now with Cloud-Aware Key Ingestion (CAKI) for Render/Docker.
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
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> str:
        """
        Elite Multi-Source Ingestion:
        1. Priority: System Environment (For Cloud/Render/Docker)
        2. Fallback: Local Config File (For Local Development)
        """
        # --- PRIORITY 1: CLOUD ENVIRONMENT (Render/Koyeb/Docker) ---
        env_key = os.getenv("GROQ_API_KEY")
        if env_key:
            logger.info("Cloud Environment Key Detected. Bypassing local files.")
            return self._sanitize_key(env_key)

        # --- PRIORITY 2: LOCAL CONFIG FILE (Laptop Mode) ---
        try:
            if not os.path.exists(self.config_path):
                # We don't raise error here anymore, just log it.
                logger.warning(f"Local config not found at {self.config_path}. Checking Env...")
                return ""
            
            encodings = ['utf-8-sig', 'utf-16', 'utf-8', 'latin-1']
            raw_content = ""
            for enc in encodings:
                try:
                    with open(self.config_path, "r", encoding=enc) as f:
                        raw_content = f.read()
                        if "=" in raw_content: break
                except: continue

            if "=" in raw_content:
                raw_key = raw_content.split("=")[1].strip()
                return self._sanitize_key(raw_key)
                
        except Exception as e:
            logger.error(f"Local Key Ingestion Failed: {e}")
            
        return ""

    def _sanitize_key(self, key: str) -> str:
        """High-precision byte-level sanitization."""
        clean_key = "".join(c for c in key if c.isprintable() and not c.isspace())
        final_key = clean_key.replace('"', '').replace("'", "")
        if not final_key.startswith("gsk_"):
            logger.error("Key Integrity Check Failed: Invalid Prefix.")
            return ""
        return final_key

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, user_prompt: str) -> str:
        if not self.api_key:
            return "SYSTEM_OFFLINE: Authentication components missing. Set GROQ_API_KEY in Environment."

        for current_model in self.model_stack:
            payload = {
                "model": current_model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are Pinak, a state-of-the-art 2026 AI for an elite CS student. Be technical, precise, and professional."
                    },
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 1024
            }

            try:
                response = requests.post(
                    self.api_url, 
                    headers=self._get_headers(), 
                    json=payload, 
                    timeout=20
                )
                
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                
                logger.warning(f"Model {current_model} failed (Status: {response.status_code}).")
                continue

            except Exception as e:
                logger.error(f"Network Error for {current_model}: {e}")
                continue

        return "STALEMATE: All models failed. Check API status or Cloud Environment Variables."

if __name__ == "__main__":
    print("--- Project Pinak: Elite 2026 Brain Node ---")
    pinak = PinakBrain()
    
    test_query = "Confirm operational readiness."
    print("Initiating Secure Connection Stack...")
    response = pinak.generate_response(test_query)
    print(f"\n[PINAK_OUTPUT]: {response}")