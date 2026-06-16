# PATCH Request - Partially Updating a Resource
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# PATCH only sends the field(s) you want to change
patch_data = {"title": "Just the Title Was Changed"}

response = requests.patch(f"{BASE_URL}/posts/1", json=patch_data)

print(response.status_code)        # 200

result = response.json()
print("title  :", result["title"])  # Just the Title Was Changed
print("body   :", result["body"])   # original body still intact
print("userId :", result["userId"]) # original userId still intact
