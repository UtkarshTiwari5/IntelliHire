from pathlib import Path


# ============================================================
# IntelliHire Project Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "models"

SKILL_ALIAS_FILE = DATA_DIR / "skill_aliases.json"
JOBS_FILE = DATA_DIR / "jobs.json"


APP_NAME = "IntelliHire"

APP_VERSION = "0.1.0"

APP_DESCRIPTION = (
    "AI-Powered Recruitment & Career Intelligence Platform"
)


# Create required directories automatically
UPLOAD_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)