import requests
import os

BASE_URL = "http://localhost:8000/api"

def test_flow():
    # Create a dummy CSV file
    with open("test_data.csv", "w") as f:
        f.write("id,name,age,score,email\n")
        f.write("1,Alice,30,85,alice@example.com\n")
        f.write("2,Bob,25,90,bob@example.com\n")
        f.write("3,Charlie,35,78,charlie@example.com\n")
        f.write("4,David,28,92,david@example.com\n")
        f.write("5,Eve,32,88,eve@example.com\n")

    try:
        # 1. Upload
        print("Testing Upload...")
        with open("test_data.csv", "rb") as f:
            files = {"file": ("test_data.csv", f, "text/csv")}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            response.raise_for_status()
            print("Upload Success:", response.json().keys())

        # 2. Analyze
        print("\nTesting Analysis...")
        response = requests.get(f"{BASE_URL}/analyze")
        response.raise_for_status()
        print("Analysis Success:", response.json().keys())

        # 3. Insights
        print("\nTesting Insights...")
        response = requests.get(f"{BASE_URL}/insights")
        response.raise_for_status()
        print("Insights Success:", response.json().keys())

        # 4. Report (Word)
        print("\nTesting Word Report...")
        response = requests.get(f"{BASE_URL}/report/word")
        response.raise_for_status()
        print("Word Report Success, size:", len(response.content))

        # 5. Report (PPT)
        print("\nTesting PPT Report...")
        response = requests.get(f"{BASE_URL}/report/ppt")
        response.raise_for_status()
        print("PPT Report Success, size:", len(response.content))

        print("\nAll backend tests passed!")
        with open("verify_success.txt", "w") as f:
            f.write("Success")

    except Exception as e:
        print(f"\nTest Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Response:", e.response.text)
    finally:
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

if __name__ == "__main__":
    test_flow()
