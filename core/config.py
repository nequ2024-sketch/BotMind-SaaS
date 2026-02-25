import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# تحميل ملف .env في حال التشغيل المحلي
load_dotenv()

class Settings(BaseSettings):
    """
    إعدادات مشروع BotMind AI - التكوين الشامل لجيش الـ 1000 روبوت
    """
    
    # --- إعدادات قاعدة البيانات والأمان ---
    # إذا كنت على Render، سيقرأ الرابط من البيئة، وإلا سيستخدم SQLite محلياً
    DATABASE_URL: str = Field(
        default="sqlite:///./botmind_database.db", 
        env="DATABASE_URL"
    )
    JWT_SECRET_KEY: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", 
        env="JWT_SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # أسبوع واحد

    # --- إعدادات الروابط (Frontend & Backend) ---
    FRONTEND_URL: str = Field(
        default="https://bot-mind-saa-s.vercel.app", 
        env="FRONTEND_URL"
    )
    
    # --- إعدادات الذكاء الاصطناعي (Gemini) ---
    # هذا المفتاح هو "مخ" الـ 1000 روبوت
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    
    # --- إعدادات الدفع (Stripe) ---
    # لتحصيل الدولارات وتفعيل الاشتراكات الاحترافية
    STRIPE_SECRET_KEY: str = Field(default="", env="STRIPE_SECRET_KEY")
    STRIPE_PRICE_ID: str = Field(default="", env="STRIPE_PRICE_ID")
    STRIPE_WEBHOOK_SECRET: str = Field(default="", env="STRIPE_WEBHOOK_SECRET")

    # --- إعدادات ميتا وإنستغرام (Meta API) ---
    # لربط السيرفر بحسابات التواصل الاجتماعي
    IG_ACCESS_TOKEN: str = Field(default="", env="IG_ACCESS_TOKEN")
    # هذا التوكن يجب أن يتطابق مع ما تضعه في صفحة Facebook Developers
    META_VERIFY_TOKEN: str = Field(
        default="botmind_webhook_secret_123", 
        env="META_VERIFY_TOKEN"
    )
    APP_ID: str = "1634584007740054" # رقم تطبيقك المعتمد

    class Config:
        # البحث عن ملف .env تلقائياً
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# تصدير نسخة واحدة من الإعدادات لاستخدامها في كل مكان
settings = Settings()

# طباعة تنبيه بسيطة عند تشغيل السيرفر للتأكد من حالة المفاتيح الأساسية
if not settings.GEMINI_API_KEY:
    print("⚠️ تحذير: GEMINI_API_KEY غير موجود! الروبوتات لن تستطيع الرد.")
if not settings.STRIPE_SECRET_KEY:
    print("⚠️ تحذير: STRIPE_SECRET_KEY غير موجود! الدفع لن يعمل.")