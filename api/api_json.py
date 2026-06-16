# JSON - Sending and Receiving JSON Data
# Start the server first: python flask_server.py
import requests
import json

BASE_URL = "http://localhost:5000"

# --- Receiving JSON ---
response = requests.get(f"{BASE_URL}/users/1")
user = response.json()              # converts JSON text → Python dict
print("type :", type(user))         # <class 'dict'>
print("name :", user["name"])
print("email:", user["email"])

# --- Sending JSON with json= argument (recommended) ---
payload = {"title": "JSON Post", "body": "Sent via json= arg", "userId": 1}
r = requests.post(f"{BASE_URL}/posts", json=payload)
print("\nPOST with json= :", r.status_code, "id:", r.json()["id"])

# --- Sending JSON manually (json.dumps + Content-Type header) ---
raw = json.dumps({"title": "Manual JSON", "body": "Sent manually", "userId": 2})
r = requests.post(
    f"{BASE_URL}/posts",
    data=raw,
    headers={"Content-Type": "application/json"},
)
print("POST manual     :", r.status_code, "id:", r.json()["id"])

# --- Pretty-printing a JSON response ---
data = r.json()
print("\nPretty-printed:")
print(json.dumps(data, indent=2))
