from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.users import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/user-info/{user_id}")
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: 
        return {"error": "User not found"}
    return {"email": user.email, "subscription_status": user.subscription_status}