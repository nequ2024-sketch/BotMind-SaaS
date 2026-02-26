import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

# استيراد كافة أجزاء المشروع
from api.payment_router import router as payment_router
from platforms.instagram.webhook import router as ig_webhook_router
from core.database import engine, Base

# إنشاء الجداول في قاعدة البيانات عند التشغيل
Base.metadata.create_all(bind=engine)

# تعريف التطبيق بإعدادات كاملة
app = FastAPI(
    title="BotMind AI - Enterprise SaaS Architecture",
    description="نظام إدارة الذكاء الاصطناعي لإنستغرام، شامل التوقيت البشري والدفعيات.",
    version="2.0.0"
)

# إعدادات الـ CORS المتقدمة لضمان تواصل Vercel مع Render بدون مشاكل
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # في الإنتاج يفضل وضع رابط Vercel الخاص بك هنا
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# تسجيل الروابط (Routers) في السيرفر الرئيسي
app.include_router(payment_router, prefix="/payment", tags=["Billing & Subscriptions"])
app.include_router(ig_webhook_router, prefix="/instagram", tags=["Meta Graph API"])

# ==========================================
# مسار المصادقة الرسمي مع فيسبوك (Meta OAuth)
# ==========================================
@app.get("/auth/instagram/login", tags=["Authentication"])
async def instagram_login():
    """توجيه المستخدم لتسجيل الدخول وإعطاء الصلاحيات للروبوتات"""
    app_id = "1634584007740054" 
    redirect_uri = "https://botmind-saas.onrender.com/auth/instagram/callback"
    
    # الصلاحيات الدقيقة المطلوبة للرد على الرسائل والتعليقات
    scopes = "instagram_basic,instagram_manage_messages,instagram_manage_comments,pages_show_list,pages_read_engagement"
    
    meta_oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}"
    
    print(f"🔗 جاري توجيه المستخدم لفيسبوك لتسجيل الدخول...")
    return RedirectResponse(url=meta_oauth_url)

@app.get("/auth/instagram/callback", tags=["Authentication"])
async def instagram_callback(code: str = None, error: str = None, error_description: str = None):
    """استقبال التوكن من ميتا بعد موافقة العميل وإعادته للوحة التحكم"""
    frontend_url = "https://bot-mind-saa-s.vercel.app"
    
    if error:
        print(f"❌ فشل تسجيل الدخول من ميتا: {error_description}")
        return RedirectResponse(url=f"{frontend_url}?login=failed&reason={error}")
        
    if code:
        print(f"✅ تسجيل دخول ناجح! الكود المستلم: {code[:10]}...")
        return RedirectResponse(url=f"{frontend_url}?login=success")
        
    return JSONResponse(status_code=400, content={"error": "Invalid callback request"})

# مسار الفحص للتأكد من عمل السيرفر على Render
@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online", 
        "project": "BotMind AI", 
        "version": "2.0.0",
        "message": "السيرفر يعمل بكفاءة. جيش الروبوتات في انتظار الأوامر! 🤖🚀"
    }

# كود التشغيل
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # التشغيل متاح لكافة الـ IP Addresses
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)