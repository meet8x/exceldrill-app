import urllib.request
import urllib.parse
import json
import mimetypes
import uuid

BASE_URL = "http://localhost:8000/api"

def upload_file(filename):
    print(f"Uploading {filename}...")
    boundary = uuid.uuid4().hex
    with open(filename, 'rb') as f:
        file_content = f.read()
    
    part_boundary = f"--{boundary}"
    
    data = []
    data.append(part_boundary)
    data.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"')
    data.append('Content-Type: text/csv')
    data.append('')
    data.append(file_content.decode('utf-8'))
    data.append(f"--{boundary}--")
    data.append('')
    
    body = "\r\n".join(data).encode('utf-8')
    
    req = urllib.request.Request(f"{BASE_URL}/upload", data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        with urllib.request.urlopen(req) as response:
            print("Upload Response:", response.read().decode('utf-8'))
    except Exception as e:
        print("Upload Failed:", e)

def test_endpoint(endpoint):
    print(f"Testing {endpoint}...")
    try:
        with urllib.request.urlopen(f"{BASE_URL}{endpoint}") as response:
            print(f"{endpoint} Response:", response.read().decode('utf-8')[:200] + "...")
    except Exception as e:
        print(f"{endpoint} Failed:", e)

def download_report(format):
    print(f"Downloading {format} report...")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/report/{format}") as response:
            content = response.read()
            print(f"Downloaded {len(content)} bytes")
            with open(f"report.{'docx' if format == 'word' else 'pptx'}", "wb") as f:
                f.write(content)
    except Exception as e:
        print(f"Download Failed:", e)

if __name__ == "__main__":
    upload_file("dummy.csv")
    test_endpoint("/analyze")
    test_endpoint("/insights")
    download_report("word")
    download_report("ppt")
