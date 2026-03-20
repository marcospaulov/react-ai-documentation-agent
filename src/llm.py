import os
import sys
from dotenv import load_dotenv
from google import genai
from src.config import CHAT_MODEL

def load_client() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERRO: defina GEMINI_API_KEY no seu arquivo .env", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)

def generate_answer(client: genai.Client, prompt: str) -> str:
    resp = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt,
    )
    return getattr(resp, "text", "").strip() or "(sem texto de resposta)"
