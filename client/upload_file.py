import requests
import sys
import os

# API_URL = os.getenv("BACKEND_URL")
API_URL = "http://localhost:8000"

def upload_file(filepath: str):
    filename = os.path.basename(filepath)

    resp = requests.post(f"{API_URL}/upload", json={"filename": filename})
    if resp.status_code != 200:
        print("Error getting pre signed url:", resp.text)
        return
    
    data = resp.json()
    upload_url = data["upload_url"]

    print(f"Uploading {filename} to {upload_url}")

    with open(filepath, "rb") as f:
        put_resp = requests.put(upload_url, data=f)

    if put_resp.status_code == 200:
        print(f"✅ File {filename} uploaded correctly.")
    else:
        print(f"❌ Error uploading file: {put_resp.status_code} {put_resp.text}")

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_file.py <file_path>")
    else:
        upload_file(sys.argv[1])