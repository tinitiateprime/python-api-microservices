# Request Headers - Sending Metadata with Your Request
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

headers = {
    "Accept":          "application/json",
    "User-Agent":      "MyPythonApp/1.0",
    "X-Custom-Header": "hello-from-client",
}

# /headers endpoint echoes back all headers the server received
response = requests.get(f"{BASE_URL}/headers", headers=headers)

print(response.status_code)        # 200

received = response.json()
print("Accept          :", received.get("Accept"))
print("User-Agent      :", received.get("User-Agent"))
print("X-Custom-Header :", received.get("X-Custom-Header"))
