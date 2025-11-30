import razorpay
import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.core.config import settings

def test_razorpay_connection():
    print(f"Testing Razorpay connection with Key ID: {settings.RAZORPAY_KEY_ID}")
    
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Try to create a dummy order
        data = {
            "amount": 100, # 1 rupee
            "currency": "INR",
            "receipt": "test_receipt_1",
            "payment_capture": 1
        }
        
        print("Attempting to create a test order...")
        order = client.order.create(data=data)
        
        print("SUCCESS! Razorpay order created successfully.")
        print(f"Order ID: {order['id']}")
        print(f"Amount: {order['amount']}")
        
    except Exception as e:
        print(f"FAILURE! Could not create Razorpay order.")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_razorpay_connection()
