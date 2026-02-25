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
# 🔴 الباب الأول: إرسال المستخدم لفيسبوك
# ==========================================
@app.get("/auth/instagram/login")
async def instagram_login():
    app_id = os.getenv("META_APP_ID", "رقم_تطبيقك_هنا")
    redirect_uri = "https://botmind-saas.onrender.com/auth/instagram/callback"
    scopes = "instagram_basic,instagram_manage_messages,instagram_manage_comments,pages_show_list,pages_read_engagement"
    meta_oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}"
    return RedirectResponse(url=meta_oauth_url)

# ==========================================
# 🟢 الباب الثاني: استقبال المستخدم بعد الموافقة
# ==========================================
@app.get("/auth/instagram/callback")
async def instagram_callback(code: str = None, error: str = None):
    # إذا رفض المستخدم أو حدث خطأ
    if error:
        return {"message": "تم إلغاء العملية ❌", "details": error}
    
    # إذا نجح الربط واستلمنا الكود (Token)
    if code:
        print(f"🎉 تم استلام كود الربط بنجاح: {code}")
        # توجيه المستخدم لموقعه على Vercel مع علامة نجاح
        frontend_dashboard = "https://bot-mind-saa-s.vercel.app?login=success"
        return RedirectResponse(url=frontend_dashboard)
    
    return {"message": "حدث خطأ غير متوقع ❌"}

# حل مشكلة الـ Not Found في الصفحة الرئيسية
@app.get("/")
def home():
    return {"message": "BotMind AI is Live & Secure! 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)