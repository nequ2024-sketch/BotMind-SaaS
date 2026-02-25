import asyncio
import random
import os
import google.generativeai as genai
from datetime import datetime, timedelta
from platforms.instagram.service import send_instagram_message
from core.database import SessionLocal
from models.users import User
from models.ai_agents import AIAgent
from models.products import Product

# ربط مفتاح جوجل جيميناي
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

BANNED_WORDS = ["عنصرية", "شتيمة", "احتيال"]
last_reply_time = datetime.utcnow()

async def process_delayed_reply(text: str, target_id: str, user_id: int):
    global last_reply_time
    
    if any(word in text.lower() for word in BANNED_WORDS): return 

    delay_seconds = random.randint(60, 180)
    target_time = max(datetime.utcnow() + timedelta(seconds=delay_seconds), last_reply_time + timedelta(minutes=2))
    last_reply_time = target_time
    
    wait_time = (target_time - datetime.utcnow()).total_seconds()
    await asyncio.sleep(wait_time)

    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        
        agent_persona = "مساعد بشري ودود"
        if user and user.selected_agent_id:
            agent = db.query(AIAgent).filter(AIAgent.id == user.selected_agent_id).first()
            if agent: agent_persona = f"{agent.name}، وأسلوبك هو: {agent.persona}"
        
        store_products = db.query(Product).filter(Product.user_id == user_id).all()
        db.close()
    except Exception as e:
        print(f"Database error: {e}")
        agent_persona = "مساعد بشري ودود"
        store_products = []

    system_prompt = f"أنت لست روبوت، أنت {agent_persona}. تتفاعل مع المتابعين على إنستغرام بلطف."
    
    if store_products:
        products_text = "\n".join([f"- {p.name}: {p.price} $" for p in store_products])
        system_prompt += f"\nملاحظة: أنت تعمل أيضاً كمندوب مبيعات. إليك منتجاتنا:\n{products_text}\nإذا سأل العميل عن السعر، أجب بناءً على هذه القائمة فقط."
    else:
        system_prompt += "\nمهمتك التفاعل الإيجابي مع الجمهور فقط. لا تعرض بيع أي شيء."

    prompt = f"{system_prompt}\n\nالعميل كتب: '{text}'\nاكتب رداً قصيراً جداً وعفوياً واستخدم إيموجي."
    
    try:
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        reply = "يا هلا فيك! تواصل معنا لأي استفسار ✨"

    await send_instagram_message(target_id, reply)