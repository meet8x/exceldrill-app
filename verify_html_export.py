import requests
import time
import os

BASE_URL = "http://localhost:8000/api"

def test_html_export():
    # 1. Login to get token
    print("1. Logging in...")
    login_data = {"username": "admin@example.com", "password": "adminpassword"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful.")
    except Exception as e:
        print(f"Login error: {e}")
        return

    # 2. Upload dummy file
    print("\n2. Uploading file...")
    # Create a dummy CSV file
    with open("test_data_html.csv", "w") as f:
        f.write("id,category,value,group\n")
        for i in range(50):
            f.write(f"{i},A,{i*2},X\n")
            f.write(f"{i+50},B,{i*3},Y\n")
            
    try:
        with open("test_data_html.csv", "rb") as f:
            files = {"file": ("test_data_html.csv", f, "text/csv")}
            upload_response = requests.post(
                f"{BASE_URL}/upload",
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

    # 3. Start HTML Report Generation
    print("\n3. Starting HTML report generation...")
    try:
        start_response = requests.post(
            f"{BASE_URL}/report/start/html",
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

    # 4. Poll for status
    print("\n4. Polling for status...")
    while True:
        status_response = requests.get(
            f"{BASE_URL}/report/status/{job_id}",
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

    # 5. Download report
    print("\n5. Downloading report...")
    try:
        download_response = requests.get(
            f"{BASE_URL}/report/download/{job_id}",
            headers=headers
        )
        
        if download_response.status_code == 200:
            with open("verified_report.html", "wb") as f:
                f.write(download_response.content)
            print("Report downloaded successfully: verified_report.html")
            print(f"File size: {os.path.getsize('verified_report.html')} bytes")
        else:
            print(f"Download failed: {download_response.text}")
    except Exception as e:
        print(f"Download error: {e}")

if __name__ == "__main__":
    test_html_export()
