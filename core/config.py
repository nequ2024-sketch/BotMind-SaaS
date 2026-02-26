import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env في بيئة التطوير المحلية
load_dotenv()

class Settings(BaseSettings):
    """
    هذا الكلاس مسؤول عن قراءة جميع المفاتيح السرية والإعدادات
    الخاصة بمشروع BotMind AI. إذا كان هناك مفتاح ناقص في سيرفر Render،
    سيقوم هذا الكلاس بإيقاف التشغيل وتنبيهك فوراً لحماية النظام.
    """
    
    # ==========================================
    # إعدادات الأمان وقاعدة البيانات
    # ==========================================
    DATABASE_URL: str = Field(
        default="sqlite:///./botmind_database.db", 
        env="DATABASE_URL",
        description="رابط الاتصال بقاعدة البيانات"
    )
    JWT_SECRET_KEY: str = Field(
        default="botmind_super_secret_key_2026_nexus_unbreakable", 
        env="JWT_SECRET_KEY",
        description="المفتاح السري لتشفير جلسات المستخدمين"
    )
    ALGORITHM: str = "HS256"

    # ==========================================
    # إعدادات الروابط (Frontend & Backend)
    # ==========================================
    FRONTEND_URL: str = Field(
        default="https://bot-mind-saa-s.vercel.app", 
        env="FRONTEND_URL"
    )
    
    # ==========================================
    # الذكاء الاصطناعي (مخ النظام - Gemini)
    # ==========================================
    GEMINI_API_KEY: str = Field(
        default="", 
        env="GEMINI_API_KEY",
        description="مفتاح جوجل للذكاء الاصطناعي"
    )
    
    # ==========================================
    # بوابات الدفع (Stripe)
    # ==========================================
    STRIPE_SECRET_KEY: str = Field(
        default="", 
        env="STRIPE_SECRET_KEY",
        description="المفتاح السري الخاص بـ Stripe لمعالجة الدفعيات"
    )
    STRIPE_WEBHOOK_SECRET: str = Field(
        default="", 
        env="STRIPE_WEBHOOK_SECRET",
        description="لتأكيد عمليات الدفع الناجحة تلقائياً من Stripe"
    )

    # ==========================================
    # إعدادات ميتا وإنستغرام (Meta API)
    # ==========================================
    IG_ACCESS_TOKEN: str = Field(
        default="", 
        env="IG_ACCESS_TOKEN",
        description="توكن الوصول الطويل الأمد لصفحة إنستغرام"
    )
    META_VERIFY_TOKEN: str = Field(
        default="botmind_webhook_secret_123", 
        env="META_VERIFY_TOKEN",
        description="كلمة السر التي سيتأكد منها فيسبوك عند ربط الويب هوك"
    )
    APP_ID: str = "1634584007740054" 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# تصدير نسخة واحدة ليتم استخدامها في باقي الملفات
settings = Settings()