# Session - Reusing Connections and Sharing Headers Across Requests
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"
API_KEY = "secret-key-123"

session = requests.Session()

# Set shared headers once — every request through this session uses them
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Accept":        "application/json",
    "User-Agent":    "SessionClient/1.0",
})

# All three calls automatically include the Authorization header
r1 = session.get(f"{BASE_URL}/protected")
print("Protected :", r1.status_code, r1.json()["message"])

r2 = session.get(f"{BASE_URL}/posts/1")
print("Posts     :", r2.status_code, r2.json()["title"])

r3 = session.get(f"{BASE_URL}/users/1")
print("Users     :", r3.status_code, r3.json()["name"])

session.close()
