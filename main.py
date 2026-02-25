from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth_router import router as auth_router
from api.payment_router import router as payment_router
from platforms.instagram.webhook import router as ig_webhook_router
from core.database import engine, Base
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

# حل مشكلة الـ Not Found في الصفحة الرئيسية
@app.get("/")
def home():
    return {"message": "BotMind AI is Live & Secure! 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
