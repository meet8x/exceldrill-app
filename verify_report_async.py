import requests
import time
import os

BASE_URL = "http://localhost:8000/api"

def test_report_generation():
    # 1. Login to get token
    print("Logging in...")
    login_data = {"username": "admin@example.com", "password": "adminpassword"}
    response = requests.post("http://localhost:8000/api/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload dummy file
    print("Uploading file...")
    with open("dummy.csv", "w") as f:
        f.write("id,category,value,group\n")
        for i in range(50):
            f.write(f"{i},A,{i*2},X\n")
            f.write(f"{i+50},B,{i*3},Y\n")
            
    with open("dummy.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload", files=files, headers=headers)
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return
    print("Upload successful.")

    # 3. Start Report Generation
    print("Starting report generation...")
    response = requests.post(f"{BASE_URL}/report/start/word", headers=headers)
    if response.status_code != 200:
        print(f"Start failed: {response.text}")
        return
    
    job_id = response.json()["job_id"]
    print(f"Job started. ID: {job_id}")

    # 4. Poll for status
    while True:
        response = requests.get(f"{BASE_URL}/report/status/{job_id}", headers=headers)
        status_data = response.json()
        print(f"Status: {status_data['status']}, Progress: {status_data['progress']}%")
        
        if status_data['status'] == 'completed':
            break
        elif status_data['status'] == 'failed':
            print(f"Job failed: {status_data.get('error')}")
            return
        
        time.sleep(1)

    # 5. Download Report
    print("Downloading report...")
    response = requests.get(f"{BASE_URL}/report/download/{job_id}", headers=headers)
    if response.status_code == 200:
        with open("verified_report.docx", "wb") as f:
            f.write(response.content)
        print("Report downloaded successfully: verified_report.docx")
    else:
        print(f"Download failed: {response.text}")

if __name__ == "__main__":
    try:
        test_report_generation()
    except Exception as e:
        print(f"Test failed with exception: {e}")
