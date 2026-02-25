from fastapi import APIRouter, Request, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.ai_engine import process_delayed_reply
from models.users import User
from models.social_accounts import SocialAccount

router = APIRouter(prefix="/instagram", tags=["Instagram"])

@router.post("/webhook")
async def receive_activity(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    data = await request.json()
    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            ig_account_id = entry.get("id")
            account = db.query(SocialAccount).filter(SocialAccount.ig_account_id == str(ig_account_id)).first()
            if not account: continue
            
            user = db.query(User).filter(User.id == account.user_id).first()
            if not user: continue
            
            # 🔴 فحص زر إيقاف البوت
            if not user.is_bot_active: continue

            if user.subscription_status == "free" and user.free_posts_used >= 3: continue
            elif user.subscription_status == "active" and user.paid_posts_used >= 10: continue

            for change in entry.get("changes", []):
                if change.get("field") == "comments":
                    text = change["value"]["text"]
                    comment_id = change["value"]["id"]
                    
                    if user.subscription_status == "free": user.free_posts_used += 1
                    else: user.paid_posts_used += 1
                    db.commit()

                    background_tasks.add_task(process_delayed_reply, text, comment_id, user.id)
                    
            for messaging in entry.get("messaging", []):
                msg_text = messaging.get("message", {}).get("text")
                sender_id = messaging.get("sender", {}).get("id")
                if msg_text:
                    background_tasks.add_task(process_delayed_reply, msg_text, sender_id, user.id)
                    
    return {"status": "SUCCESS"}