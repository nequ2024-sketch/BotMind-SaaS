import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./botmind_database.db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")
    IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN", "")
    META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "botmind_webhook_secret_123")

settings = Settings()