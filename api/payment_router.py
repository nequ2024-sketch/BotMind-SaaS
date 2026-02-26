from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import stripe
from core.config import settings

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY

# قاعدة بيانات محاكاة (Mock DB) لإدارة باقات المستخدمين
# في بيئة الإنتاج سيتم استبدالها بـ SQLAlchemy أو PostgreSQL
database_simulation = {
    "user_1": {
        "is_subscribed": False, 
        "free_posts_used": 0,   # الحد 3
        "paid_posts_used": 0    # الحد 10
    }
}

@router.get("/check-limits/{user_id}")
async def check_user_limits(user_id: str):
    """
    يتم استدعاء هذا المسار قبل تشغيل البوت على أي بوست جديد 
    للتحقق من رصيد العميل بناءً على خطة البزنس.
    """
    user = database_simulation.get(user_id, {"is_subscribed": False, "free_posts_used": 0, "paid_posts_used": 0})
    
    # حالة 1: العميل مجاني واستنفذ الـ 3 بوستات
    if not user["is_subscribed"] and user["free_posts_used"] >= 3:
        return {"allowed": False, "status": "UPGRADE_REQUIRED", "message": "انتهت البوستات المجانية (3/3). يرجى الاشتراك بـ 50$ شهرياً."}
    
    # حالة 2: العميل مشترك واستنفذ الـ 10 بوستات
    if user["is_subscribed"] and user["paid_posts_used"] >= 10:
        return {"allowed": False, "status": "PAY_EXTRA", "message": "تجاوزت حد الـ 10 بوستات. يرجى دفع 5$ للبوست الإضافي."}
        
    return {"allowed": True, "status": "OK", "message": "رصيدك يسمح بتشغيل البوت."}


# ==========================================
# بوابات الدفع الرسمية (Stripe - بطاقات ائتمان)
# ==========================================
@router.get("/subscribe/card/{user_id}")
async def pay_monthly_subscription(user_id: str):
    """توليد جلسة دفع لاشتراك 50$ (10 بوستات)"""
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email="customer@example.com", # يمكن تمريره ديناميكياً
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'الاشتراك الاحترافي الشهري - BotMind AI',
                        'description': 'تفعيل الذكاء الاصطناعي للرد على 10 بوستات'
                    },
                    'unit_amount': 5000, # 50.00 USD
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{settings.FRONTEND_URL}?payment=success&user={user_id}",
            cancel_url=f"{settings.FRONTEND_URL}?payment=cancel",
        )
        return RedirectResponse(url=checkout_session.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/extra-post/card/{user_id}")
async def pay_extra_post(user_id: str):
    """توليد جلسة دفع لشراء بوست إضافي بقيمة 5$"""
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'شحن بوست إضافي واحد ⚡',
                    },
                    'unit_amount': 500, # 5.00 USD
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{settings.FRONTEND_URL}?payment=extra_success&user={user_id}",
            cancel_url=f"{settings.FRONTEND_URL}?payment=cancel",
        )
        return RedirectResponse(url=checkout_session.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# بوابة الدفع الرقمية (الكريبتو - USDT)
# ==========================================
@router.get("/pay/usdt/{user_id}")
async def pay_with_usdt(user_id: str, type: str = "monthly"):
    """
    تزويد العميل بعنوان محفظة TRC20 لدفع العملات الرقمية
    """
    amount = "50" if type == "monthly" else "5"
    wallet_trc20 = "TQsXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # ضع محفظتك الحقيقية هنا
    
    return {
        "status": "pending_crypto",
        "payment_method": "USDT (Network: TRC20)",
        "amount_required": f"{amount} USDT",
        "wallet_address": wallet_trc20,
        "instructions": "قم بنسخ عنوان المحفظة وتحويل المبلغ المطلوب تماماً. سيتم تفعيل حسابك بمجرد تأكيد الشبكة (عادة يستغرق 1-3 دقائق).",
        "warning": "الرجاء التأكد من اختيار شبكة TRC20 (Tron) لتجنب فقدان الأموال."
    }