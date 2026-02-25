import httpx
from core.config import settings

async def send_instagram_message(recipient_id: str, message_text: str):
    # التعديل هنا: غيرنا الرابط لـ facebook بدل instagram لأنه هذا المعتمد من ميتا للرسائل
    url = "https://graph.facebook.com/v18.0/me/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.IG_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            
            # التعديل هنا: أضفنا رسائل تنبيه عشان لو فشل الإرسال، السيرفر يكتبلنا السبب!
            if response.status_code != 200:
                print(f"❌ خطأ من ميتا أثناء الإرسال: {response.text}")
            else:
                print(f"✅ تم إرسال رد الذكاء الاصطناعي بنجاح إلى {recipient_id}!")
                
            return response.json()
    except Exception as e:
        print(f"❌ خطأ في الاتصال بسيرفرات ميتا: {e}")