from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth_router import router as auth_router
from api.payment_router import router as payment_router
from platforms.instagram.webhook import router as ig_webhook_router
from core.database import engine, Base
from fastapi.responses import RedirectResponse
import os
import uvicorn

# إنشاء الداتابيز فوراً
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BotMind AI - Global")

# تفعيل الـ CORS ليعمل Vercel مع Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(payment_router, prefix="/payment")
app.include_router(ig_webhook_router, prefix="/instagram")

# ==========================================
# 🔴 الباب الجديد: مسار تسجيل الدخول لإنستغرام
# ==========================================
@app.get("/auth/instagram/login")
async def instagram_login():
    # سحب رقم التطبيق من Render (سنضيفه لاحقاً في الإعدادات)
    app_id = os.getenv("META_APP_ID", "رقم_تطبيقك_هنا")
    
    # رابط العودة بعد الموافقة
    redirect_uri = "https://botmind-saas.onrender.com/auth/instagram/callback"
    
    # الصلاحيات المطلوبة
    scopes = "instagram_basic,instagram_manage_messages,instagram_manage_comments,pages_show_list,pages_read_engagement"
    
    # رابط صفحة الموافقة الزرقاء من ميتا
    meta_oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}"
    
    # نقل المستخدم فوراً لصفحة ميتا
    return RedirectResponse(url=meta_oauth_url)

# حل مشكلة الـ Not Found في الصفحة الرئيسية
@app.get("/")
def home():
    return {"message": "BotMind AI is Live & Secure! 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)