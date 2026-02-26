import httpx
from core.config import settings

async def send_instagram_message(recipient_id: str, message_text: str):
    """
    تقوم هذه الدالة بإرسال رسالة مباشرة (DM) إلى المستخدم على إنستغرام
    باستخدام Graph API الخاص بـ Meta.
    """
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
        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.post(url, headers=headers, json=payload)
            res_data = res.json()
            
            if res.status_code == 200:
                print(f"✅ تم إرسال الرسالة الخاصة بنجاح إلى المعرف: {recipient_id}")
            else:
                error_msg = res_data.get("error", {}).get("message", "Unknown Meta Error")
                print(f"❌ خطأ من سيرفرات ميتا أثناء إرسال الرسالة: {error_msg}")
    except httpx.ConnectError:
        print("❌ فشل الاتصال بسيرفرات ميتا (تأكد من اتصال الإنترنت أو إعدادات الجدار الناري).")
    except Exception as e:
        print(f"❌ خطأ برمجي غير متوقع في خدمة الرسائل: {e}")


async def reply_to_instagram_comment(comment_id: str, message_text: str):
    """
    تقوم هذه الدالة بالرد مباشرة على تعليق محدد (Reply to Comment)
    على بوستات صفحة إنستغرام الخاصة بالعميل.
    """
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    
    headers = {
        "Authorization": f"Bearer {settings.IG_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": message_text
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.post(url, headers=headers, json=payload)
            res_data = res.json()
            
            if res.status_code == 200:
                print(f"✅ تم الرد بنجاح على التعليق رقم: {comment_id}")
            else:
                error_msg = res_data.get("error", {}).get("message", "Unknown Meta Error")
                print(f"❌ خطأ من سيرفرات ميتا أثناء الرد على التعليق: {error_msg}")
    except httpx.ConnectError:
        print("❌ فشل الاتصال بسيرفرات ميتا (تأكد من حالة شبكة السيرفر).")
    except Exception as e:
        print(f"❌ خطأ برمجي غير متوقع في خدمة التعليقات: {e}")