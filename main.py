import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

# استيراد الـ Routers الخاصة بالمشروع
from api.auth_router import router as auth_router
from api.payment_router import router as payment_router
from platforms.instagram.webhook import router as ig_webhook_router
from core.database import engine, Base

# --- إعداد قاعدة البيانات ---
# هذا السطر يضمن إنشاء الجداول فور تشغيل السيرفر على Render
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BotMind AI - Global Enterprise SaaS",
    description="نظام إدارة جيش الـ 1000 روبوت والردود الذكية",
    version="1.0.0"
)

# --- إعدادات الـ CORS (الأمان) ---
# تفعيل الربط الكامل بين Vercel و Render لمنع أخطاء المتصفح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج يفضل تحديد رابط Vercel الخاص بك
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ربط المسارات (Routers) ---
app.include_router(auth_router, prefix="/auth", tags=["Security"])
app.include_router(payment_router, prefix="/payment", tags=["Billing"])
app.include_router(ig_webhook_router, prefix="/instagram", tags=["Social Media"])

# ==========================================
# 🔴 بوابة تسجيل الدخول (Meta OAuth Gateway)
# ==========================================
@app.get("/auth/instagram/login")
async def instagram_login():
    """
    توجيه المستخدم إلى صفحة ميتا الرسمية لطلب الصلاحيات
    """
    app_id = "1634584007740054" # رقم تطبيقك المثبت في ميتا
    # الرابط الذي سيعود إليه المستخدم بعد الموافقة
    redirect_uri = "https://botmind-saas.onrender.com/auth/instagram/callback"
    
    # الصلاحيات المطلوبة للرد على الرسائل والتعليقات
    scopes = [
        "instagram_basic",
        "instagram_manage_messages",
        "instagram_manage_comments",
        "pages_show_list",
        "pages_read_engagement"
    ]
    scope_str = ",".join(scopes)
    
    meta_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={app_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope_str}"
    )
    
    print(f"🔗 جاري تحويل المستخدم إلى Meta عبر التطبيق: {app_id}")
    return RedirectResponse(url=meta_url)

# ==========================================
# 🟢 بوابة العودة (Callback Handler)
# ==========================================
@app.get("/auth/instagram/callback")
async def instagram_callback(code: str = None, error: str = None, error_description: str = None):
    """
    استقبال المستخدم بعد الموافقة وتوجيهه إلى لوحة التحكم في Vercel
    """
    frontend_url = "https://bot-mind-saa-s.vercel.app"

    # في حال رفض المستخدم أو حدوث خطأ تقني من ميتا
    if error:
        print(f"❌ خطأ في ربط إنستغرام: {error_description}")
        return RedirectResponse(url=f"{frontend_url}?login=failed&reason={error}")
    
    # في حال النجاح والحصول على كود الوصول
    if code:
        print(f"✅ تم استلام كود الربط بنجاح: {code[:10]}***")
        # التوجيه للداشبورد مع علامة النجاح لفتحها تلقائياً
        return RedirectResponse(url=f"{frontend_url}?login=success")
    
    return JSONResponse(status_code=400, content={"message": "طلب غير مكتمل أو مفقود"})

@app.get("/")
async def root_status():
    return {
        "status": "online",
        "project": "BotMind AI",
        "region": "Zarqa Hub - Render Node",
        "message": "جيش الـ 1000 روبوت جاهز للعمل 🤖🚀"
    }

if __name__ == "__main__":
    # تشغيل السيرفر محلياً أو على السحابة
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)