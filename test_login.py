import requests
import json

# Test login endpoint
url = "http://localhost:8000/api/login"
data = {
    "username": "admin@example.com",
    "password": "adminpassword"
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✓ Login successful!")
        token_data = response.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:50]}...")
    else:
        print("\n✗ Login failed!")
        
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to backend. Is it running on http://localhost:8000?")
except Exception as e:
    print(f"Error: {e}")
