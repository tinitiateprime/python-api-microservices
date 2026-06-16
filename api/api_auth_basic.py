# Authentication - Basic Auth (Username and Password)
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"
USERNAME = "alice"
PASSWORD = "password123"

# --- Without credentials --- should get 401
r = requests.get(f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}")
print("Without auth:", r.status_code)              # 401

# --- With correct credentials --- should get 200
r = requests.get(
    f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}",
    auth=(USERNAME, PASSWORD)
)
print("With auth   :", r.status_code)              # 200
data = r.json()
print("Authenticated:", data["authenticated"])     # True
print("User        :", data["user"])               # alice
