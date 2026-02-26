import asyncio
import random
import time
import google.generativeai as genai
from core.config import settings
from platforms.instagram.service import send_instagram_message, reply_to_instagram_comment

# تهيئة الذكاء الاصطناعي فور تشغيل السيرفر
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# متغير عالمي لضمان فاصل الـ 120 ثانية الإجباري لحماية الحساب من الحظر
last_reply_time = 0

async def process_smart_reply(
    text: str, 
    sender_id: str, 
    is_comment: bool = False,
    persona_name: str = "شاب عفوي ومحب للحياة", 
    keywords: list = ["رابط بالبايو", "خصم رهيب", "يا هلا"]
):
    """
    هذه الدالة هي العقل المدبر لـ BotMind AI.
    تستقبل النص، تحدد التوقيت البشري المناسب، تمرر النص لـ Gemini مع أوامر صارمة،
    ثم ترسل الرد النهائي لإنستغرام (إما كتعليق أو رسالة خاصة).
    """
    global last_reply_time
    source_type = "تعليق" if is_comment else "رسالة خاصة"
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📥 {source_type} جديد مستلم من {sender_id}: {text}")
    
    # ==========================================
    # 1. نظام التوقيت البشري العشوائي (Human Delay)
    # ==========================================
    # انتظار عشوائي بين 60 ثانية (دقيقة) و 180 ثانية (3 دقائق)
    human_delay = random.randint(60, 180) 
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ⏳ تم تفعيل التأخير البشري: النظام سينتظر {human_delay} ثانية.")
    await asyncio.sleep(human_delay)
    
    # ==========================================
    # 2. نظام مانع الحظر (Rate Limiter)
    # ==========================================
    current_time = time.time()
    time_since_last_reply = current_time - last_reply_time
    if time_since_last_reply < 120:
        wait_time = 120 - time_since_last_reply
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚦 زحمة! حماية الحساب مفعلة. تأجيل الرد {int(wait_time)} ثانية.")
        await asyncio.sleep(wait_time)
    
    # تحديث العداد
    last_reply_time = time.time()

    # ==========================================
    # 3. هندسة الأوامر الاحترافية (Prompt Engineering)
    # ==========================================
    keywords_str = "، ".join(keywords) if keywords else "لا يوجد"
    
    prompt = f"""
    أنت إنسان حقيقي وتدير صفحة إنستغرام بمهارة. شخصيتك التي تمثلها هي: "{persona_name}".
    يجب أن تدمج بعض هذه الكلمات في ردك بعفوية شديدة وبدون تصنع: [{keywords_str}].
    
    القواعد الذهبية الصارمة:
    1. ابتعد تماماً عن اللغة العربية الفصحى المعقدة والردود الآلية المبرمجة مثل ("مرحباً بك"، "كيف أساعدك اليوم"، "أنا هنا لخدمتك").
    2. استخدم العامية الدارجة، واجعل الرد قصيراً جداً (سطر واحد فقط) وكأنك تكتبه بسرعة من هاتفك المحمول.
    3. لا تضع نقطة (.) في نهاية الجملة دائماً لتبدو طبيعياً. استخدم الإيموجي بشكل خفيف (🔥، 😍، 😎، 🙏).
    4. الانعكاس اللغوي الذكي (Bilingual): 
       - إذا كان النص المكتوب بالعربي، رد بلهجة دارجة لطيفة (يا غالي، أبشر، من عيوني، تم). 
       - إذا كان النص المكتوب بالإنجليزي، رد بـ Slang شبابي طبيعي (Gotchu, Bro, Check DM, Sure thing).
    5. الحماية الأخلاقية المطلقة: إذا كان النص يحتوي على أي شتيمة، إهانة، تنمر، عنصرية، أو محتوى غير أخلاقي، يُمنع الرد تماماً. أرجع هذه الكلمة فقط بحروف كبيرة: IGNORE_COMMENT
    
    نوع التفاعل: {source_type}
    نص المتابع: "{text}"
    الرد البشري:
    """
    
    try:
        # ==========================================
        # 4. توليد الرد من الذكاء الاصطناعي
        # ==========================================
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🧠 جاري معالجة الرد عبر Gemini...")
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
        
        # تفعيل الفلترة الأخلاقية إذا اكتشف الذكاء الاصطناعي مخالفة
        if "IGNORE_COMMENT" in ai_reply or "ignore_comment" in ai_reply.lower():
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🗑️ تم تجاهل الـ {source_type} بسبب احتوائه على محتوى مسيء.")
            return {"status": "ignored", "reason": "offensive_content"}
            
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🤖 الرد الجاهز للإرسال: {ai_reply}")
        
        # ==========================================
        # 5. التوجيه بناءً على نوع الحدث (رسالة أم تعليق)
        # ==========================================
        if is_comment:
            await reply_to_instagram_comment(sender_id, ai_reply)
        else:
            await send_instagram_message(sender_id, ai_reply)
            
        return {"status": "success", "reply": ai_reply}
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ خطأ حرج في محرك الذكاء الاصطناعي: {e}")
        # رد طوارئ في حال تعطل سيرفرات جوجل
        fallback_reply = "شيك الخاص يا غالي 🔥" if is_comment else "يا هلا بك، رح نرد عليك بأقرب وقت! 🙏"
        if is_comment:
            await reply_to_instagram_comment(sender_id, fallback_reply)
        else:
            await send_instagram_message(sender_id, fallback_reply)
        return {"status": "error_fallback_used"}