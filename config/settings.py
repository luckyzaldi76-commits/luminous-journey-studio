from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Luminous Journey Studio"
VERSION = "0.3.0"

# ==========================================================
# PATH
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = PROJECT_DIR / "01_DATABASE"
PROMPT_DIR = PROJECT_DIR / "02_MASTER_PROMPT"
OUTPUT_DIR = PROJECT_DIR / "exports"
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

OPENROUTER_TEMPERATURE = 0.7

# ==========================================================
# TOKEN LIMIT
# ==========================================================

STAGE1_MAX_TOKENS = 700
STAGE2_MAX_TOKENS = 250
STAGE3_MAX_TOKENS = 600
STAGE4_MAX_TOKENS = 150

OPENROUTER_MAX_TOKENS = STAGE1_MAX_TOKENS

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