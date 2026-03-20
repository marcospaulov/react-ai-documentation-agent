import os
from pathlib import Path

CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")

ROOT_DIR = Path(__file__).parent.parent.resolve()
