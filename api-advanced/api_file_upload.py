# File Upload - Sending a file to the server using multipart/form-data
# Start the server first: python api-advanced/flask_server_advanced.py
import requests
import io

BASE_URL = "http://localhost:5001"

# --- Upload from disk ---
# Uncomment if you have a real file to upload:
# with open("report.pdf", "rb") as f:
#     r = requests.post(f"{BASE_URL}/upload", files={"file": f})

# --- Upload from memory (no real file needed) ---
# io.BytesIO lets us create an in-memory "file"
fake_file = io.BytesIO(b"Hello, this is the file content!")
fake_file.name = "hello.txt"

r = requests.post(
    f"{BASE_URL}/upload",
    files={"file": ("hello.txt", fake_file, "text/plain")}
    #           ^tuple: (filename, file-like object, content-type)
)

print("Status      :", r.status_code)     # 200
result = r.json()
print("Filename    :", result["filename"])
print("Size (bytes):", result["size_bytes"])
print("Content-Type:", result["content_type"])

# --- Upload a file alongside other form fields ---
fake_file.seek(0)                          # rewind before re-reading
r = requests.post(
    f"{BASE_URL}/upload",
    files={"file": ("hello.txt", fake_file, "text/plain")},
    data={"description": "my upload"}     # extra form field alongside the file
)
print("\nWith extra field:", r.status_code)
