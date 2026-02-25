from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.ai_agents import AIAgent
from models.users import User

router = APIRouter(prefix="/agents", tags=["AI Agents"])

@router.get("/")
def get_all_agents(db: Session = Depends(get_db)):
    return db.query(AIAgent).limit(20).all()

@router.post("/select/{user_id}/{agent_id}")
def select_agent(user_id: int, agent_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.selected_agent_id = agent_id
        db.commit()
        return {"message": "تم تعيين الشخصية بنجاح!"}
    return {"error": "المستخدم غير موجود"}

@router.get("/status/{user_id}")
def get_bot_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user: return {"is_bot_active": user.is_bot_active}
    return {"error": "المستخدم غير موجود"}

@router.post("/toggle-bot/{user_id}")
def toggle_bot(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_bot_active = not user.is_bot_active
        db.commit()
        status = "مفعل 🟢" if user.is_bot_active else "متوقف 🔴"
        return {"message": f"تم تغيير حالة البوت إلى: {status}", "is_bot_active": user.is_bot_active}
    return {"error": "المستخدم غير موجود"}