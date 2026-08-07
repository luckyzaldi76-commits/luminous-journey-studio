import os
from pathlib import Path

from dotenv import load_dotenv

# ==========================================================
# PATH
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = PROJECT_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Luminous Journey Studio"

VERSION = "0.4.1"

# ==========================================================
# AI PROVIDER
# ==========================================================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "auto",
).strip().lower()

USE_MOCK = (
    os.getenv(
        "USE_MOCK",
        "False",
    )
    .strip()
    .lower()
    == "true"
)

# ==========================================================
# PATH
# ==========================================================

DATABASE_DIR = PROJECT_DIR / "01_DATABASE"

PROMPT_DIR = PROJECT_DIR / "02_MASTER_PROMPT"

OUTPUT_DIR = PROJECT_DIR / "exports"

LOG_DIR = PROJECT_DIR / "logs"

# ==========================================================
# OPENROUTER
# ==========================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "",
).strip()

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5.5",
).strip()

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

OPENROUTER_TEMPERATURE = 0.7

# ==========================================================
# GEMINI
# ==========================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "",
).strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-pro",
).strip()

# ==========================================================
# TOKEN
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

# ==========================================================
# RUNTIME
# ==========================================================

ENABLE_EVENT_BUS = True

ENABLE_ANALYTICS = True

ENABLE_CACHE = False

# ==========================================================
# EXPORT
# ==========================================================

DEFAULT_EXPORT_FORMAT = "markdown"

# ==========================================================
# DEBUG
# ==========================================================

print("=" * 60)
print("CONFIG LOADED")
print(f".env         : {ENV_FILE}")
print(f"AI_PROVIDER  : {AI_PROVIDER}")
print(f"USE_MOCK     : {USE_MOCK}")
print(f"GEMINI MODEL : {GEMINI_MODEL}")
print(f"OPENROUTER   : {OPENROUTER_MODEL}")
print("=" * 60)