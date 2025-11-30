import razorpay
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.api import deps
from backend.app.core.config import settings
from backend.app.models.user import User

router = APIRouter()

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class OrderCreateRequest(BaseModel):
    plan_id: str = "lifetime" # '24h', 'monthly', 'lifetime'

class OrderResponse(BaseModel):
    id: str
    amount: int
    currency: str
    key_id: str
    plan_id: str

PLANS = {
    "24h": {"amount": 99, "duration": timedelta(hours=24)},
    "monthly": {"amount": 499, "duration": timedelta(days=30)},
    "lifetime": {"amount": 1999, "duration": None}
}

@router.post("/create-order", response_model=OrderResponse)
def create_order(
    request: OrderCreateRequest,
    current_user: User = Depends(deps.get_current_user),
):
    print(f"🔵 Creating order for user: {current_user.email} (ID: {current_user.id}), Plan: {request.plan_id}")
    
    if request.plan_id not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan ID")
    
    plan = PLANS[request.plan_id]
    
    try:
        data = {
            "amount": plan["amount"] * 100, # Convert to paise
            "currency": "INR",
            "receipt": f"receipt_order_{current_user.id}_{request.plan_id}",
            "payment_capture": 1,
            "notes": {
                "plan_id": request.plan_id,
                "user_id": str(current_user.id),
                "user_email": current_user.email
            }
        }
        print(f"🔵 Razorpay order data: {data}")
        order = client.order.create(data=data)
        print(f"✅ Razorpay order created: {order['id']}")
        
        return {
            "id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key_id": settings.RAZORPAY_KEY_ID,
            "plan_id": request.plan_id
        }
    except Exception as e:
        print(f"❌ Error creating Razorpay order: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Failed to create order: {str(e)}")

class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    plan_id: str

@router.post("/verify-payment")
def verify_payment(
    request: PaymentVerifyRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    print(f"🔵 Verifying payment for user: {current_user.email}, Plan: {request.plan_id}")
    
    try:
        # Verify signature
        params_dict = {
            'razorpay_order_id': request.razorpay_order_id,
            'razorpay_payment_id': request.razorpay_payment_id,
            'razorpay_signature': request.razorpay_signature
        }
        
        print(f"🔵 Verifying Razorpay signature...")
        client.utility.verify_payment_signature(params_dict)
        print(f"✅ Razorpay signature verified")
        
        # Update user status based on plan
        if request.plan_id not in PLANS:
             raise HTTPException(status_code=400, detail="Invalid plan ID")

        plan = PLANS[request.plan_id]
        current_user.is_paid = True
        current_user.plan_type = request.plan_id
        
        if plan["duration"]:
            expiry = datetime.utcnow() + plan["duration"]
            current_user.plan_expiry = expiry.isoformat()
        else:
            current_user.plan_expiry = None # Lifetime
        
        print(f"🔵 Updating user in database...")
        db.commit()
        db.refresh(current_user)
        print(f"✅ User updated: is_paid={current_user.is_paid}, plan_type={current_user.plan_type}")
        
        # Send Welcome Email
        try:
            from backend.app.services.email_service import EmailService
            email_service = EmailService()
            # Use full_name if available, otherwise fallback
            user_name = current_user.full_name if current_user.full_name else "Valued User"
            email_service.send_welcome_premium_email(current_user.email, user_name)
            print(f"✅ Welcome email sent to {current_user.email}")
        except Exception as e:
            print(f"⚠️ Failed to send welcome email: {e}")

        return {"status": "success", "message": "Payment verified successfully"}
    except razorpay.errors.SignatureVerificationError as e:
        print(f"❌ Signature verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        print(f"❌ Error verifying payment: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Payment verification error: {str(e)}")
