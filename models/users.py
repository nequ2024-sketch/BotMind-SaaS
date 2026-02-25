from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    stripe_customer_id = Column(String, unique=True, nullable=True)
    subscription_status = Column(String, default="free") 
    free_posts_used = Column(Integer, default=0) 
    paid_posts_used = Column(Integer, default=0) 
    
    selected_agent_id = Column(Integer, nullable=True) 
    is_bot_active = Column(Boolean, default=True) # زر التحكم
    
    created_at = Column(DateTime, default=datetime.utcnow)