from fastapi import APIRouter, Request, Response
import asyncio
from core.ai_engine import process_delayed_reply

router = APIRouter()

# الكلمة السرية التي اعتمدناها في Meta
VERIFY_TOKEN = "botmind_webhook_secret_123"

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return Response(content=params.get("hub.challenge"), media_type="text/plain")
    return Response(content="Verification failed", status_code=403)

@router.post("/webhook")
async def handle_messages(request: Request):
    data = await request.json()
    
    if "entry" in data:
        for entry in data["entry"]:
            # رصد الرسائل الخاصة (DMs)
            if "messaging" in entry:
                for msg in entry["messaging"]:
                    if "message" in msg and "text" in msg["message"]:
                        sender_id = msg["sender"]["id"]
                        text = msg["message"].get("text")
                        print(f"📩 رسالة جديدة للذكاء الاصطناعي: {text}")
                        # إرسال المهمة للمخ في الخلفية (user_id=1 للتجربة)
                        asyncio.create_task(process_delayed_reply(text, sender_id, user_id=1))
                        
            # رصد التعليقات (Comments)
            elif "changes" in entry:
                for change in entry["changes"]:
                    if change["field"] == "comments":
                        text = change["value"].get("text")
                        comment_id = change["value"].get("id")
                        print(f"💬 تعليق جديد للذكاء الاصطناعي: {text}")
                        # الرد على التعليق في الخلفية
                        asyncio.create_task(process_delayed_reply(text, comment_id, user_id=1))
    
    # نرد على Meta فوراً بـ OK عشان ما يعطونا خطأ
    return {"status": "ok"}