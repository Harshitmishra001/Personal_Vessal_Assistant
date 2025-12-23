from pathlib import Path

APP_NAME = "PersonalVesselAssistant"
APP_VERSION = "0.1.0"

BASE_DIR = Path.home() / ".pva"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "pva.db"
