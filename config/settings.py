import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# PATH
# ==========================================================

PROJECT_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)

ENV_FILE = Path(
    os.getenv(
        "LUMINOUS_JOURNEY_ENV_FILE",
        str(PROJECT_DIR / ".env"),
    )
)

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)


# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Luminous Journey Studio"

VERSION = "0.6.0"


# ==========================================================
# AI
# ==========================================================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "auto",
).strip().lower()


USE_MOCK = (
    os.getenv(
        "USE_MOCK",
        os.getenv(
            "MOCK",
            "False",
        ),
    )
    .strip()
    .lower()
    in {
        "1",
        "true",
        "yes",
        "on",
    }
)


# ==========================================================
# DIRECTORY
# ==========================================================

DATABASE_DIR = PROJECT_DIR / "01_DATABASE"

PROMPT_DIR = PROJECT_DIR / "02_MASTER_PROMPT"

TEMPLATE_DIR = PROJECT_DIR / "templates"

OUTPUT_DIR = PROJECT_DIR / "exports"

LOG_DIR = PROJECT_DIR / "logs"

CONFIG_DIR = PROJECT_DIR / "config"


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

OPENROUTER_TEMPERATURE = float(
    os.getenv(
        "OPENROUTER_TEMPERATURE",
        "0.7",
    )
)


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

STAGE1_MAX_TOKENS = int(
    os.getenv(
        "STAGE1_MAX_TOKENS",
        "700",
    )
)

STAGE2_MAX_TOKENS = int(
    os.getenv(
        "STAGE2_MAX_TOKENS",
        "250",
    )
)

STAGE3_MAX_TOKENS = int(
    os.getenv(
        "STAGE3_MAX_TOKENS",
        "600",
    )
)

STAGE4_MAX_TOKENS = int(
    os.getenv(
        "STAGE4_MAX_TOKENS",
        "150",
    )
)

OPENROUTER_MAX_TOKENS = (
    STAGE1_MAX_TOKENS
)


# ==========================================================
# REQUEST
# ==========================================================

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "300",
    )
)

MAX_RETRY = int(
    os.getenv(
        "MAX_RETRY",
        "5",
    )
)


# ==========================================================
# LANGUAGE
# ==========================================================

LANGUAGES = (
    "IND",
    "ENG",
    "ESP",
    "ZHT",
    "ZHS",
    "PINYIN",
)


# ==========================================================
# RUNTIME
# ==========================================================

ENABLE_EVENT_BUS = True

ENABLE_ANALYTICS = True

ENABLE_CACHE = False


# ==========================================================
# PROVIDER HEALTH
# ==========================================================

PROVIDER_HEALTH_FILE = Path(
    os.getenv(
        "PROVIDER_HEALTH_FILE",
        str(
            CONFIG_DIR
            / "provider_health.json"
        ),
    )
)

PROVIDER_HEALTH_DEFAULT_COOLDOWN = int(
    os.getenv(
        "PROVIDER_HEALTH_DEFAULT_COOLDOWN",
        "60",
    )
)

PROVIDER_HEALTH_QUOTA_COOLDOWN = int(
    os.getenv(
        "PROVIDER_HEALTH_QUOTA_COOLDOWN",
        "300",
    )
)

PROVIDER_HEALTH_SERVER_COOLDOWN = int(
    os.getenv(
        "PROVIDER_HEALTH_SERVER_COOLDOWN",
        "30",
    )
)


# ==========================================================
# EXPORT
# ==========================================================

DEFAULT_EXPORT_FORMAT = "markdown"


# ==========================================================
# DEBUG
# ==========================================================

DEBUG = (
    os.getenv(
        "DEBUG",
        "True",
    )
    .strip()
    .lower()
    == "true"
)


if DEBUG:

    print("=" * 60)

    print(APP_NAME)

    print("=" * 60)

    print(
        f"Version        : {VERSION}"
    )

    print(
        f".env           : {ENV_FILE}"
    )

    print(
        f"AI Provider    : {AI_PROVIDER}"
    )

    print(
        f"Mock           : {USE_MOCK}"
    )

    print(
        f"Gemini Model   : {GEMINI_MODEL}"
    )

    print(
        f"OpenRouter     : {OPENROUTER_MODEL}"
    )

    print("=" * 60)