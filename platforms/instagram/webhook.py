from fastapi import APIRouter, Request, Response
import asyncio
from core.ai_engine import process_delayed_reply

router = APIRouter()
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
            # رصد رسائل الـ DM
            if "messaging" in entry:
                for msg in entry["messaging"]:
                    if "message" in msg and "text" in msg["message"]:
                        # تشغيل محرك الذكاء الاصطناعي
                        asyncio.create_task(process_delayed_reply(msg["message"]["text"], msg["sender"]["id"], 1))
            # رصد التعليقات
            elif "changes" in entry:
                for change in entry["changes"]:
                    if change.get("field") == "comments":
                        text = change["value"].get("text")
                        comment_id = change["value"].get("id")
                        asyncio.create_task(process_delayed_reply(text, comment_id, 1))
    return {"status": "ok"}