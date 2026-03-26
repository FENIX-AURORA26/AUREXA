import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "aurexa_boreal_db.json"

APP_NAME = "AUREXA_BOREAL"
SUPPORT_EMAIL = os.getenv("AUREXA_SUPPORT_TARGET", "luna_site@fenix-boreal.com.br")
REMOTE_API_BASE_URL = os.getenv("AUREXA_API_BASE_URL", "https://aurexa-api.onrender.com")
LOCAL_API_BASE_URL = os.getenv("AUREXA_LOCAL_API_BASE_URL", "http://127.0.0.1:5000")

OWNER_EMAIL = os.getenv("AUREXA_OWNER_EMAIL", "luna_site@fenix-boreal.com.br")
OWNER_PASSWORD = os.getenv("AUREXA_OWNER_PASSWORD", "AurexaBoreal@123")
