from pathlib import Path

# ==========================================================
# ROOT PROJECT (PORTABLE)
# ==========================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_DIR = PROJECT_DIR / "01_DATABASE"

# ==========================================================
# MASTER PROMPT
# ==========================================================

PROMPT_DIR = APP_DIR / "02_MASTER_PROMPT"

PROMPT_FILE = (
    PROMPT_DIR
    / "LUMINOUS JOURNEY DAILY PRODUCTION MASTER PROMPT v5LZ.docx"
)

# ==========================================================
# OUTPUT
# ==========================================================

OUTPUT_DIR = APP_DIR / "OUTPUTS"

# ==========================================================
# KNOWLEDGE
# ==========================================================

KNOWLEDGE_DIR = APP_DIR / "KNOWLEDGE"
DATASET_DIR = APP_DIR / "datasets"
RESOURCE_DIR = APP_DIR / "resources"
EXPORT_DIR = APP_DIR / "exports"
LOG_DIR = APP_DIR / "logs"

# ==========================================================
# CREATE FOLDERS
# ==========================================================

FOLDERS = [
    OUTPUT_DIR,
    KNOWLEDGE_DIR,
    DATASET_DIR,
    RESOURCE_DIR,
    EXPORT_DIR,
    LOG_DIR,
]

def create_folders():
    for folder in FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)

    print("Luminous Journey Configuration Loaded")


create_folders()

# ==========================================================
# LANGUAGES
# ==========================================================

LANGUAGES = [
    "IND",
    "ENG",
    "ESP",
    "ZHT",
    "ZHS",
    "PINYIN",
]