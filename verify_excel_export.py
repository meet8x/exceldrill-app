import requests
import time
import os
import sys

# Configuration
BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@example.com"
LOGIN_PASSWORD = "adminpassword"

def verify_excel_export():
    print("1. Logging in...")
    try:
        auth_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={"username": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
        )
        if auth_response.status_code != 200:
            print(f"Login failed: {auth_response.text}")
            return
        
        token = auth_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful.")
    except Exception as e:
        print(f"Login error: {e}")
        return

    print("\n2. Uploading file...")
    # Create a dummy CSV file
    with open("test_data.csv", "w") as f:
        f.write("id,name,age,salary,department\n")
        for i in range(1, 21):
            f.write(f"{i},Employee{i},{25+i},{50000+i*1000},Dept{i%3}\n")
    
    try:
        with open("test_data.csv", "rb") as f:
            files = {"file": ("test_data.csv", f, "text/csv")}
            upload_response = requests.post(
                f"{BASE_URL}/api/upload",
                headers=headers,
                files=files
            )
            
        if upload_response.status_code != 200:
            print(f"Upload failed: {upload_response.text}")
            return
        print("Upload successful.")
    except Exception as e:
        print(f"Upload error: {e}")
        return

    print("\n3. Starting Excel report generation...")
    try:
        start_response = requests.post(
            f"{BASE_URL}/api/report/start/excel",
            headers=headers
        )
        
        if start_response.status_code != 200:
            print(f"Start report failed: {start_response.text}")
            return
            
        job_id = start_response.json()["job_id"]
        print(f"Job started. ID: {job_id}")
    except Exception as e:
        print(f"Start report error: {e}")
        return

    print("\n4. Polling for status...")
    while True:
        status_response = requests.get(
            f"{BASE_URL}/api/report/status/{job_id}",
            headers=headers
        )
        status_data = status_response.json()
        status = status_data["status"]
        progress = status_data["progress"]
        
        print(f"Status: {status}, Progress: {progress}%")
        
        if status == "completed":
            break
        elif status == "failed":
            print(f"Job failed: {status_data.get('error')}")
            return
            
        time.sleep(1)

    print("\n5. Downloading report...")
    try:
        download_response = requests.get(
            f"{BASE_URL}/api/report/download/{job_id}",
            headers=headers
        )
        
        if download_response.status_code == 200:
            with open("verified_report.xlsx", "wb") as f:
                f.write(download_response.content)
            print("Report downloaded successfully: verified_report.xlsx")
        else:
            print(f"Download failed: {download_response.text}")
    except Exception as e:
        print(f"Download error: {e}")

if __name__ == "__main__":
    verify_excel_export()
