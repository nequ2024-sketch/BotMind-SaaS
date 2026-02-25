from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.social_accounts import SocialAccount

router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.post("/connect-instagram/{user_id}")
def connect_instagram(user_id: int, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(SocialAccount.user_id == user_id).first()
    if not account:
        account = SocialAccount(user_id=user_id, ig_account_id=f"ig_{user_id}", followers_count=5500)
        db.add(account)
        db.commit()
    return {"message": "تم ربط حساب إنستغرام!"}