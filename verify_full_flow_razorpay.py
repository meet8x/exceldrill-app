import requests
import time
import os

BASE_URL = "http://localhost:8000/api"
AUTH_URL = f"{BASE_URL}/auth"
PAYMENT_URL = f"{BASE_URL}/payment"

def create_dummy_csv():
    with open("test_data.csv", "w") as f:
        f.write("id,name,age,score,email\n")
        f.write("1,Alice,30,85,alice@example.com\n")
        f.write("2,Bob,25,90,bob@example.com\n")
        f.write("3,Charlie,35,78,charlie@example.com\n")

def verify_full_flow():
    print("Starting Full Flow Verification...")
    create_dummy_csv()
    
    email = f"fullflow_{int(time.time())}@example.com"
    password = "password123"

    # 1. Register
    print(f"\n1. Registering user: {email}")
    resp = requests.post(f"{AUTH_URL}/register", json={"email": email, "password": password})
    if resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        return
    print("Registration successful")

    # 1.5 Manually Verify User (Bypass Email Verification for Test)
    print("Manually verifying user for testing...")
    from backend.app.db.session import SessionLocal
    from backend.app.models.user import User
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
        print(f"User {email} manually verified.")
    db.close()

    # 2. Login
    print("\n2. Logging in")
    resp = requests.post(f"{AUTH_URL}/login", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")

    # 3. Upload File
    print("\n3. Uploading File")
    with open("test_data.csv", "rb") as f:
        files = {"file": ("test_data.csv", f, "text/csv")}
        resp = requests.post(f"{BASE_URL}/upload", files=files, headers=headers) # Note: headers might need adjustment for multipart, but requests handles it usually if we don't set Content-Type manually
        # Actually, for Authorization we need to pass headers. requests merges them.
    
    if resp.status_code != 200:
        print(f"Upload failed: {resp.text}")
        return
    print("Upload successful")

    # 4. Analyze
    print("\n4. Analyzing Data")
    resp = requests.get(f"{BASE_URL}/analyze", headers=headers)
    if resp.status_code != 200:
        print(f"Analysis failed: {resp.text}")
        return
    print("Analysis successful")

    # 5. Try Download (Should Fail)
    print("\n5. Verifying Download Protection (Free User)")
    # The endpoint is POST /report/start/{format}
    resp = requests.post(f"{BASE_URL}/report/start/word", headers=headers)
    if resp.status_code == 403:
        print("Download correctly forbidden")
    else:
        print(f"Unexpected status: {resp.status_code} - {resp.text}")
        return

    # 6. Create Order
    print("\n6. Creating Razorpay Order")
    resp = requests.post(f"{PAYMENT_URL}/create-order", json={"amount": 900}, headers=headers)
    if resp.status_code != 200:
        print(f"Order creation failed: {resp.text}")
        return
    order_id = resp.json()['id']
    print(f"Order created: {order_id}")

    # 7. Verify Payment (Mock)
    print("\n7. Verifying Payment")
    verify_data = {
        "razorpay_order_id": order_id,
        "razorpay_payment_id": "pay_fake_full_flow",
        "razorpay_signature": "fake_signature",
        "plan_id": "lifetime"
    }
    resp = requests.post(f"{PAYMENT_URL}/verify-payment", json=verify_data, headers=headers)
    
    if resp.status_code == 200:
        print("Payment verified successfully")
    else:
        print(f"Payment verification failed as expected (Signature mismatch): {resp.text}")
        # Manually upgrade user for testing step 8
        print("Manually upgrading user to premium for testing...")
        from backend.app.db.session import SessionLocal
        from backend.app.models.user import User
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_paid = True
            user.plan_type = "lifetime"
            db.commit()
            print(f"User {email} manually upgraded to premium.")
        db.close()

    # 8. Try Download (Should Succeed)
    print("\n8. Verifying Download (Premium User)")
    # Start report generation
    resp = requests.post(f"{BASE_URL}/report/start/word", headers=headers)
    if resp.status_code != 200:
        print(f"Report generation start failed: {resp.status_code} - {resp.text}")
        return
    
    job_id = resp.json()['job_id']
    print(f"Report job started: {job_id}")
    
    # Poll for completion
    print("Polling for report completion...")
    for _ in range(10):
        time.sleep(1)
        resp = requests.get(f"{BASE_URL}/report/status/{job_id}", headers=headers)
        status = resp.json()['status']
        print(f"Status: {status}")
        if status == 'completed':
            break
        if status == 'failed':
            print(f"Report generation failed: {resp.json().get('error')}")
            return
            
    # Download
    resp = requests.get(f"{BASE_URL}/report/download/{job_id}", headers=headers)
    if resp.status_code == 200:
        print("Download successful")
    else:
        print(f"Download failed: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    try:
        verify_full_flow()
    finally:
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
