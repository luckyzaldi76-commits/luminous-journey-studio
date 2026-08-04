from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Luminous Journey Studio"
VERSION = "0.2.0"

# ==========================================================
# PATH
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = PROJECT_DIR / "01_DATABASE"
PROMPT_DIR = PROJECT_DIR / "02_MASTER_PROMPT"
OUTPUT_DIR = PROJECT_DIR / "11_SCRIPT" / "OUTPUTS"
LOG_DIR = PROJECT_DIR / "logs"

# ==========================================================
# OPENROUTER
# ==========================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5.5",
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

OPENROUTER_MAX_TOKENS = 512

OPENROUTER_TEMPERATURE = 0.7

# ==========================================================
# REQUEST
# ==========================================================

REQUEST_TIMEOUT = 300

MAX_RETRY = 5

# ==========================================================
# LANGUAGE
# ==========================================================

LANGUAGES = [
    "IND",
    "ENG",
    "ESP",
    "ZHT",
    "ZHS",
    "PINYIN",
]