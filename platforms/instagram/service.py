import httpx
from core.config import settings

async def send_instagram_message(recipient_id: str, message_text: str):
    url = "https://graph.instagram.com/v18.0/me/messages"
    headers = {
        "Authorization": f"Bearer {settings.IG_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)