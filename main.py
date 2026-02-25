import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base

from api import auth_router, oauth_router, payment_router, agent_router, product_router
from platforms.instagram import webhook

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexus Protocol - BotMind AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(oauth_router.router)
app.include_router(payment_router.router)
app.include_router(agent_router.router)
app.include_router(product_router.router)
app.include_router(webhook.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)