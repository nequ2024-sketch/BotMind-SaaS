from sqlalchemy import Column, Integer, String
from core.database import Base, SessionLocal, engine
import random

class AIAgent(Base):
    __tablename__ = "ai_agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    persona = Column(String)
    status = Column(String, default="active")

Base.metadata.create_all(bind=engine)

first_names = ["Elon", "Keanu", "Robert", "Chris", "Tom", "Leonardo"]
last_names = ["Musk", "Reeves", "Downey", "Evans", "Cruise", "DiCaprio"]
personas = ["ودود ومرح", "رسمي واحترافي", "ساخر بذكاء", "عبقري وهادئ"]

def seed_1000_bots():
    db = SessionLocal()
    if db.query(AIAgent).count() > 0: return
    agents = [AIAgent(name=f"{random.choice(first_names)} {random.choice(last_names)} {i}", persona=random.choice(personas)) for i in range(1000)]
    db.bulk_save_objects(agents)
    db.commit()
    print("🚀 تم زرع 1000 روبوت بنجاح!")

if __name__ == "__main__":
    seed_1000_bots()