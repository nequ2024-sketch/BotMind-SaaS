from fastapi import APIRouter, Request, Response

router = APIRouter()

# الكلمة السرية التي اعتمدناها في Meta
VERIFY_TOKEN = "botmind_webhook_secret_123"

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    
    return Response(content="Verification failed", status_code=403)

@router.post("/webhook")
async def handle_messages(request: Request):
    data = await request.json()
    
    # التحقق من نوع البيانات القادمة من Meta
    if "entry" in data:
        for entry in data["entry"]:
            # 1. إذا كان التحديث تعليقاً على منشور
            if "changes" in entry:
                for change in entry["changes"]:
                    if change["field"] == "comments":
                        comment_text = change["value"].get("text")
                        comment_id = change["value"].get("id")
                        print(f"💬 تعليق جديد تم رصده: {comment_text}")
                        # هنا سنضيف لاحقاً كود رد الذكاء الاصطناعي على التعليق
            
            # 2. إذا كان التحديث رسالة خاصة (DM)
            elif "messaging" in entry:
                for message_event in entry["messaging"]:
                    if "message" in message_event:
                        sender_id = message_event["sender"]["id"]
                        text = message_event["message"].get("text")
                        print(f"📩 رسالة خاصة جديدة من {sender_id}: {text}")
                        # هنا نرسل الرد الآلي عبر الخاص
    
    return {"status": "ok"}