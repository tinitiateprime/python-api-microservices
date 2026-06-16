# POST Request - Creating a New Resource
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

new_post = {
    "title":  "My New Post",
    "body":   "This is the content of my new post.",
    "userId": 1,
}

response = requests.post(f"{BASE_URL}/posts", json=new_post)

print(response.status_code)        # 201 Created

created = response.json()
print("New post ID :", created["id"])
print("Title       :", created["title"])
print("Body        :", created["body"])
