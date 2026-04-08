import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("APP_DATA_DIR", str(BASE_DIR / "data")))
GENERATED_DIR = Path(os.getenv("APP_GENERATED_DIR", str(BASE_DIR / "generated_outputs")))
DATA_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = Path(os.getenv("APP_DB_PATH", str(DATA_DIR / "app.db")))
