# GET Request - Filtering with Query Parameters
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# Filter posts to only those belonging to userId=1
params = {"userId": 1}

response = requests.get(f"{BASE_URL}/posts", params=params)

# The actual URL that was sent
print(response.url)                # http://localhost:5000/posts?userId=1
print(response.status_code)        # 200

posts = response.json()
print(f"Posts for userId=1: {len(posts)}")

for post in posts:
    print(f"  [{post['id']}] {post['title']}")
