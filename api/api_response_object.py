# Response Object - Exploring What You Get Back
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/users/1")

# Status code number
print("status_code :", response.status_code)

# True if 200-399, False for 4xx/5xx
print("ok          :", response.ok)

# Raw response body as plain text
print("text        :", response.text[:60])

# Response body parsed as a Python dict or list
data = response.json()
print("name        :", data["name"])
print("email       :", data["email"])

# HTTP headers returned by the server
print("Content-Type:", response.headers["Content-Type"])

# How long the round trip took
print("elapsed (s) :", response.elapsed.total_seconds())
