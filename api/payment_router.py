import stripe
from fastapi import APIRouter, Depends, HTTPException
from core.config import settings

router = APIRouter(prefix="/payment", tags=["Payment"])
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/subscribe/{user_id}")
async def create_subscription(user_id: int):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'], mode='subscription',
            line_items=[{'price': settings.STRIPE_PRICE_ID, 'quantity': 1}],
            client_reference_id=str(user_id),
            success_url=settings.FRONTEND_URL + "?success=true",
            cancel_url=settings.FRONTEND_URL + "?canceled=true",
        )
        return {"checkout_url": session.url}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.post("/pay-extra-post/{user_id}")
async def pay_extra_post(user_id: int):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'], mode='payment',
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'بوست إضافي'}, 'unit_amount': 500}, 'quantity': 1}],
            client_reference_id=f"extra_{user_id}",
            success_url=settings.FRONTEND_URL + "?extra=true",
            cancel_url=settings.FRONTEND_URL,
        )
        return {"checkout_url": session.url}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.post("/crypto-pay/{user_id}")
async def create_crypto_payment(user_id: int):
    return {"payment_url": f"https://crypto-gateway.com/pay?user={user_id}&amount=50&currency=USDT"}