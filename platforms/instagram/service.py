import httpx
from core.config import settings

async def send_instagram_message(recipient_id: str, message_text: str):
    """
    إرسال رسالة ذكاء اصطناعي عبر Meta Graph API
    """
    # الرابط الرسمي المعتمد من ميتا لرسائل الـ Messenger/Instagram
    url = "https://graph.facebook.com/v18.0/me/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.IG_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    
    print(f"📤 جاري إرسال رد إلى المعرف: {recipient_id}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            if response.status_code != 200:
                error_msg = response_data.get("error", {}).get("message", "Unknown Error")
                print(f"❌ خطأ من ميتا: {error_msg}")
                return {"status": "error", "reason": error_msg}
            
            print(f"✅ تم الإرسال بنجاح! معرف الرسالة: {response_data.get('message_id')}")
            return {"status": "success", "data": response_data}
            
    except Exception as e:
        print(f"❌ خطأ غير متوقع في نظام الإرسال: {e}")
        return {"status": "error", "message": str(e)}