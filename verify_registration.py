import requests
import sys

BASE_URL = "http://localhost:8000/api/auth"

def register_user():
    email = "test_user@example.com"
    password = "password123"
    
    print(f"Attempting to register user: {email}")
    
    try:
        response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
        if response.status_code == 200:
            print("Registration successful!")
            print(response.json())
            return True
        else:
            print(f"Registration failed with status code: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Is it running?")
        return False

if __name__ == "__main__":
    if register_user():
        sys.exit(0)
    else:
        sys.exit(1)
