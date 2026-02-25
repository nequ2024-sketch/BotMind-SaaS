from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    platform = Column(String, default="instagram")
    ig_account_id = Column(String, unique=True, index=True)
    followers_count = Column(Integer, default=0)