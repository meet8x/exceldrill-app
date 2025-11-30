import requests
import sys

BASE_URL = "http://localhost:8000/api/auth"

def test_login():
    email = "test_login_user@example.com"
    password = "testpassword123"

    # 1. Register
    print(f"Registering user: {email}")
    try:
        reg_resp = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
        if reg_resp.status_code == 200:
            print("Registration successful")
        elif reg_resp.status_code == 400 and "already exists" in reg_resp.text:
            print("User already exists, proceeding to login")
        else:
            print(f"Registration failed: {reg_resp.status_code} - {reg_resp.text}")
            return
    except Exception as e:
        print(f"Registration request failed: {e}")
        return

    # 2. Login
    print(f"Logging in user: {email}")
    try:
        # Note: OAuth2PasswordRequestForm expects form data, not JSON
        login_data = {
            "username": email,
            "password": password
        }
        login_resp = requests.post(f"{BASE_URL}/login", data=login_data)
        
        if login_resp.status_code == 200:
            print("Login successful!")
            print(f"Response: {login_resp.json()}")
        else:
            print(f"Login failed: {login_resp.status_code} - {login_resp.text}")
            
    except Exception as e:
        print(f"Login request failed: {e}")

if __name__ == "__main__":
    test_login()
