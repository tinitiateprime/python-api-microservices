# PUT Request - Replacing a Resource Entirely
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# PUT replaces the whole resource — every field must be sent
updated_post = {
    "title":  "Completely New Title",
    "body":   "Completely new body text.",
    "userId": 2,
}

response = requests.put(f"{BASE_URL}/posts/1", json=updated_post)

print(response.status_code)        # 200

result = response.json()
print("id     :", result["id"])
print("title  :", result["title"])
print("body   :", result["body"])
print("userId :", result["userId"])
