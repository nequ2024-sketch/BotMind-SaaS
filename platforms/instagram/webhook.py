from fastapi import APIRouter, Request, Response

router = APIRouter()

# يجب أن يكون نفس الرمز الذي كتبتيه في Meta
VERIFY_TOKEN = "botmind_webhook_secret_123"

@router.get("/webhook")
async def verify_webhook(request: Request):
    # Meta ترسل هذه البيانات للتأكد من هوية السيرفر
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        # إذا كانت كلمة السر صحيحة، نرد بـ challenge ليعمل الربط
        return Response(content=challenge, media_type="text/plain")
    
    return Response(content="Verification failed", status_code=403)

@router.post("/webhook")
async def handle_messages(request: Request):
    # هنا سيتم استقبال الرسائل الحقيقية لاحقاً
    data = await request.json()
    print(f"Received message: {data}")
    return {"status": "ok"}