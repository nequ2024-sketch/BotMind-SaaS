from sqlalchemy import Column, Integer, String
from core.database import Base

class AIAgent(Base):
    __tablename__ = "ai_agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    persona = Column(String)
    status = Column(String, default="active")