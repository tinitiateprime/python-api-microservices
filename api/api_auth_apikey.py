# Authentication - API Key (Bearer Token)
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"
API_KEY = "secret-key-123"         # must match flask_server.py

# --- Without the key --- should get 401
r = requests.get(f"{BASE_URL}/protected")
print("Without key:", r.status_code, r.json())     # 401 Unauthorized

# --- With the correct key --- should get 200
headers = {"Authorization": f"Bearer {API_KEY}"}
r = requests.get(f"{BASE_URL}/protected", headers=headers)
print("With key   :", r.status_code, r.json())     # 200 + secret data
