import requests
import uuid
import os

BASE_URL = "http://localhost:8000"
EMAIL = f"test_user_{uuid.uuid4()}@example.com"
PASSWORD = "password123"

def run_verification():
    print(f"Testing with user: {EMAIL}")
    
    # 1. Register
    print("\n1. Registering...")
    resp = requests.post(f"{BASE_URL}/api/auth/register", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        return
    print("Registration successful")

    # 2. Login
    print("\n2. Logging in...")
    resp = requests.post(f"{BASE_URL}/api/auth/login", data={"username": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful, token received")

    # 3. Check Status (Should be free)
    print("\n3. Checking status...")
    resp = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    user_data = resp.json()
    print(f"User status: is_paid={user_data['is_paid']}")
    if user_data['is_paid']:
        print("Error: User should not be paid yet")
        return

    # 4. Upload Data
    print("\n4. Uploading data...")
    with open("dummy.csv", "rb") as f:
        files = {"file": ("dummy.csv", f, "text/csv")}
        resp = requests.post(f"{BASE_URL}/api/upload", files=files, headers=headers) # Note: upload might not need auth, but let's see
        # Actually, looking at endpoints.py, upload does NOT depend on current_user, but it uses a session-based processor.
        # The current implementation of get_processor uses a global dictionary.
        # Since we are using the same process, it should be fine.
        # However, in a real app, we should probably associate data with the user.
        # For now, let's assume the session is shared or we are the only user.
    if resp.status_code != 200:
        print(f"Upload failed: {resp.text}")
        return
    print("Upload successful")

    # 5. Try to download report (Should fail)
    print("\n5. Trying to download report (expecting failure)...")
    resp = requests.get(f"{BASE_URL}/api/report/word", headers=headers)
    if resp.status_code == 403:
        print("Success: Download denied as expected")
    else:
        print(f"Error: Expected 403, got {resp.status_code}")
        return

    # 6. Simulate Payment (Manual DB Update)
    print("\n6. Simulating Payment (Manual DB Update)...")
    from backend.app.db.session import SessionLocal
    from backend.app.models.user import User
    
    db = SessionLocal()
    user = db.query(User).filter(User.email == EMAIL).first()
    if user:
        user.is_paid = True
        db.commit()
        print("User manually upgraded to paid.")
    else:
        print("Error: User not found in DB")
        return
    db.close()

    # 7. Check Status Again
    print("\n7. Checking status again...")
    resp = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    user_data = resp.json()
    print(f"User status: is_paid={user_data['is_paid']}")
    if not user_data['is_paid']:
        print("Error: User should be paid now")
        return

    # 8. Download report (Should succeed)
    print("\n8. Downloading report (expecting success)...")
    resp = requests.get(f"{BASE_URL}/api/report/word", headers=headers)
    if resp.status_code == 200:
        print("Success: Report downloaded")
    else:
        print(f"Error: Expected 200, got {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    # Add project root to sys.path
    import sys
    import os
    sys.path.append(os.getcwd())
    
    run_verification()
