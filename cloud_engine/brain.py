import os
import requests
import json
from typing import Optional, Dict, List, Any

class PinakBrain:
    """
    ULTIMATE 2026 EDITION - Project Pinak Core Brain.
    Combines high-tier security sanitization with autonomous model fallback.
    Designed for elite CS implementation with zero-failure tolerance.
    """

    def __init__(self, config_path: str = "secure_keys/config.txt"):
        self.config_path = config_path
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # 2026 ELITE MODELS: Primary is Llama 3.3, with ultra-stable fallbacks
        self.model_stack = [
            "llama-3.3-70b-versatile", 
            "llama-3.1-70b-versatile", 
            "llama3-70b-8192"
        ]
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> str:
        """Advanced byte-level sanitization for secure key ingestion."""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Missing config at {self.config_path}")
            
            # Phase 1: Multi-encoding ingestion
            encodings = ['utf-8-sig', 'utf-16', 'utf-8', 'latin-1']
            raw_content = ""
            for enc in encodings:
                try:
                    with open(self.config_path, "r", encoding=enc) as f:
                        raw_content = f.read()
                        if "=" in raw_content: break
                except: continue

            if "=" not in raw_content:
                raise ValueError("Format Error: GROQ_API_KEY=value expected.")
                
            # Phase 2: High-precision sanitization
            raw_key = raw_content.split("=")[1].strip()
            clean_key = "".join(c for c in raw_key if c.isprintable() and not c.isspace())
            final_key = clean_key.replace('"', '').replace("'", "")
            
            if not final_key.startswith("gsk_"):
                raise ValueError("Key Integrity Check Failed: Invalid Prefix.")
                
            return final_key
        except Exception as e:
            print(f"[CRITICAL ERROR] Brain Initialization Failed: {e}")
            return ""

    def _get_headers(self) -> Dict[str, str]:
        """Generates production-standard sanitized headers."""
        return {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json"
        }

    def generate_response(self, user_prompt: str) -> str:
        """
        Executes an autonomous request with model-fallback redundancy.
        Ensures the system stays online even if the primary model is throttled.
        """
        if not self.api_key:
            return "SYSTEM_OFFLINE: Authentication components missing."

        # Model Fallback Loop: Trying each model in the stack
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
                
                # If 400 or other error, log it and try the next model in the stack
                print(f"[RECOVERY] Model {current_model} failed (Status: {response.status_code}). Switching...")
                continue

            except Exception as e:
                print(f"[NETWORK LOG] Attempt failed for {current_model}: {e}")
                continue

        return "STALEMATE: All models in the stack failed. Check API Key status or Network Firewall."

if __name__ == "__main__":
    print("--- Project Pinak: Elite 2026 Brain Node ---")
    pinak = PinakBrain()
    
    test_query = "Confirm operational readiness and identify your current active model."
    
    print("Initiating Secure Connection Stack...")
    response = pinak.generate_response(test_query)
    print(f"\n[PINAK_OUTPUT]: {response}")