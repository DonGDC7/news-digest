import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent

REQUIRED_SETTINGS = (
    "ANTHROPIC_API_KEY",
    "GMAIL_ADDRESS",
    "GMAIL_APP_PASSWORD",
    "RECIPIENT_EMAIL",
)


def load_config() -> dict[str, str]:
    load_dotenv(ROOT / ".env")
    return {name: os.getenv(name, "").strip() for name in REQUIRED_SETTINGS}
