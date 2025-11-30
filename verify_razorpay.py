import requests
import time

BASE_URL = "http://localhost:8000/api"
AUTH_URL = f"{BASE_URL}/auth"
PAYMENT_URL = f"{BASE_URL}/payment"

def verify_auth_flow():
    print("Verifying Auth Flow...")
    email = f"testuser_{int(time.time())}@example.com"
    password = "password123"

    # 1. Register
    print(f"1. Registering user: {email}")
    resp = requests.post(f"{AUTH_URL}/register", json={"email": email, "password": password})
    if resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        return None, None
    print("Registration successful")

    # 2. Login
    print("2. Logging in")
    resp = requests.post(f"{AUTH_URL}/login", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return None, None
    token = resp.json()["access_token"]
    print("Login successful, token received")

    return token, email

def verify_razorpay_flow(token):
    print("\nVerifying Razorpay Flow...")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Check initial status (should be free)
    print("1. Checking initial status")
    resp = requests.get(f"{AUTH_URL}/me", headers=headers)
    user_data = resp.json()
    if user_data["is_paid"]:
        print("User should not be paid initially")
        return False
    print("User is initially free (correct)")

    # 2. Create Order
    print("2. Creating Razorpay Order")
    resp = requests.post(f"{PAYMENT_URL}/create-order", json={"amount": 900}, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to create order: {resp.text}")
        return False
    
    order_data = resp.json()
    print(f"Order created: {order_data['id']}")
    
    # 3. Verify Payment (Mock Signature)
    # Since we can't easily generate a valid Razorpay signature without the secret (which we have, but the library does it),
    # and we can't make a real payment here.
    # We will just verify that the endpoint exists and handles invalid signatures correctly.
    
    print("3. Testing Payment Verification (Invalid Signature)")
    verify_data = {
        "razorpay_order_id": order_data['id'],
        "razorpay_payment_id": "pay_fake_123",
        "razorpay_signature": "fake_signature"
    }
    resp = requests.post(f"{PAYMENT_URL}/verify-payment", json=verify_data, headers=headers)
    
    if resp.status_code == 400 and "Payment verification failed" in resp.text:
        print("Verification correctly failed for fake signature")
    else:
        print(f"Unexpected response for fake signature: {resp.status_code} - {resp.text}")

    # 4. Try to access protected route (download) - Should fail
    print("4. Verifying protected download (should fail)")
    resp = requests.get(f"{BASE_URL}/report/word", headers=headers)
    if resp.status_code == 403:
        print("Download correctly forbidden for free user")
    else:
        print(f"Unexpected status code for download: {resp.status_code}")

    return True

if __name__ == "__main__":
    token, email = verify_auth_flow()
    if token:
        verify_razorpay_flow(token)
