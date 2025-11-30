import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_otp_flow():
    print("Testing OTP Flow...")
    email = "otp_user@example.com"
    password = "password123"
    full_name = "OTP User"
    
    # 1. Register
    print("\n1. Registering user...")
    payload = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Registration successful.")
            if user_data.get("is_verified") is False:
                print("✅ User is initially unverified.")
            else:
                print("❌ User should be unverified initially.")
                return False
        elif response.status_code == 400 and "already exists" in response.text:
             print("⚠️ User already exists. Cannot test full OTP flow cleanly.")
             return False
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False

    # 2. Try Login (Should Fail)
    print("\n2. Attempting login before verification...")
    data = {"username": email, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login", data=data)
    if response.status_code == 400 and "Email not verified" in response.json().get("detail"):
        print("✅ Login failed as expected (Email not verified).")
    else:
        print(f"❌ Login should have failed but got: {response.status_code} - {response.text}")
        return False

    # 3. Fetch OTP from DB
    print("\n3. Fetching OTP from DB...")
    from backend.app.db.session import SessionLocal
    from backend.app.models.user import User
    
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    otp = user.otp
    db.close()
    
    print(f"✅ OTP fetched: {otp}")

    # 4. Verify OTP
    print("\n4. Verifying OTP...")
    verify_payload = {"email": email, "otp": otp}
    response = requests.post(f"{BASE_URL}/auth/verify-otp", json=verify_payload)
    if response.status_code == 200:
        print("✅ OTP verified successfully.")
    else:
        print(f"❌ OTP verification failed: {response.status_code} - {response.text}")
        return False

    # 5. Login Again (Should Success)
    print("\n5. Attempting login after verification...")
    response = requests.post(f"{BASE_URL}/auth/login", data=data)
    if response.status_code == 200:
        print("✅ Login successful.")
        return True
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    if test_otp_flow():
        print("\n✅ OTP Flow (Registration & Login Block) verified.")
        sys.exit(0)
    else:
        sys.exit(1)
