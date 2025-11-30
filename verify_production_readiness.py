import requests
import sys

print("Script started...")

BASE_URL = "http://localhost:8000/api"

def test_registration_with_name():
    print("Testing registration with full name...")
    email = "john.doe@example.com"
    password = "password123"
    full_name = "John Doe"
    
    payload = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 200:
            user_data = response.json()
            if user_data.get("full_name") == full_name:
                print("✅ Registration successful. Full name saved correctly.")
                return True
            else:
                print(f"❌ Registration successful but full_name mismatch. Got: {user_data.get('full_name')}")
                return False
        elif response.status_code == 400 and "already exists" in response.text:
             print("⚠️ User already exists. Skipping registration.")
             return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False

def test_login_and_me():
    print("\nTesting login and /me endpoint...")
    email = "john.doe@example.com"
    password = "password123"
    
    try:
        # Login
        data = {
            "username": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
        token = response.json()["access_token"]
        print("✅ Login successful.")
        
        # Get Me
        headers = {"Authorization": f"Bearer {token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if me_response.status_code == 200:
            user_data = me_response.json()
            if user_data.get("full_name") == "John Doe":
                 print("✅ /me endpoint returned correct full name.")
                 return True
            else:
                 print(f"❌ /me endpoint returned wrong name: {user_data.get('full_name')}")
                 return False
        else:
            print(f"❌ /me request failed: {me_response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error during login/me check: {e}")
        return False

def test_admin_login():
    print("\nTesting admin login (admin@example.com)...")
    email = "admin@example.com"
    password = "adminpassword"
    
    try:
        # Login
        data = {
            "username": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=data)
        if response.status_code != 200:
            print(f"❌ Admin login failed: {response.status_code} - {response.text}")
            return False
            
        token = response.json()["access_token"]
        print("✅ Admin login successful.")
        
        # Get Me
        headers = {"Authorization": f"Bearer {token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ Admin /me endpoint successful. Name: {user_data.get('full_name')}")
            return True
        else:
            print(f"❌ Admin /me request failed: {me_response.status_code} - {me_response.text}")
            return False

    except Exception as e:
        print(f"❌ Error during admin login check: {e}")
        return False

if __name__ == "__main__":
    if test_registration_with_name() and test_login_and_me() and test_admin_login():
        print("\n✅ All Production Readiness checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Checks failed.")
        sys.exit(1)
