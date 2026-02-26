from fastapi import APIRouter, Request, HTTPException
from core.config import settings
from core.ai_engine import process_smart_reply
import asyncio

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    نقطة النهاية (Endpoint) الخاصة بتأكيد الويب هوك مع منصة Meta Developers.
    فيسبوك يقوم بإرسال طلب GET ويجب أن نرد عليه بالرمز (challenge).
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.META_VERIFY_TOKEN:
        print("\n✅ [الويب هوك] تم توثيق الاتصال بنجاح مع سيرفرات ميتا!")
        return int(challenge)
        
    print("❌ [الويب هوك] محاولة ربط فاشلة (كلمة السر غير متطابقة).")
    raise HTTPException(status_code=403, detail="Verification token mismatch or invalid mode")


@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    هنا نستقبل جميع التحديثات الحية من إنستغرام (رسائل جديدة، تعليقات جديدة).
    يتم تشريح الـ JSON المعقد لفصل التعليقات عن الرسائل وتوجيهها للذكاء الاصطناعي.
    """
    try:
        payload = await request.json()
    except Exception as e:
        print(f"❌ [الويب هوك] خطأ في قراءة الـ JSON: {e}")
        return {"status": "error", "message": "Invalid JSON"}
        
    if payload.get("object") == "instagram":
        for entry in payload.get("entry", []):
            
            # ==========================================
            # مسار أ: معالجة الرسائل الخاصة (Direct Messages)
            # ==========================================
            if "messaging" in entry:
                for messaging_event in entry["messaging"]:
                    # التأكد من وجود نص داخل الرسالة (وليست صورة أو إشعار قراءة)
                    if "message" in messaging_event and "text" in messaging_event["message"]:
                        sender_id = messaging_event["sender"]["id"]
                        text = messaging_event["message"]["text"]
                        
                        # نستخدم asyncio لتشغيل الرد في الخلفية لكي لا يتعطل سيرفر FastAPI
                        asyncio.create_task(
                            process_smart_reply(text=text, sender_id=sender_id, is_comment=False)
                        )
            
            # ==========================================
            # مسار ب: معالجة التعليقات على المنشورات (Comments)
            # ==========================================
            elif "changes" in entry:
                for change_event in entry["changes"]:
                    if change_event.get("field") == "comments":
                        comment_data = change_event.get("value", {})
                        comment_text = comment_data.get("text")
                        comment_id = comment_data.get("id")
                        is_reply = comment_data.get("is_reply", False)
                        
                        # يجب أن نتأكد أن التعليق ليس رداً من البوت نفسه لمنع الحلقة اللانهائية (Infinite Loop)
                        if comment_text and comment_id and not is_reply:
                            asyncio.create_task(
                                process_smart_reply(text=comment_text, sender_id=comment_id, is_comment=True)
                            )
                            
    # يجب دائماً إرجاع رد سريع 200 لفيسبوك حتى لا يظن أن سيرفرنا معطل
    return {"status": "EVENT_RECEIVED"}