# GET Request - Fetching a List of Resources
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/posts")

print(response.status_code)        # 200

posts = response.json()            # list of dicts
print(f"Total posts: {len(posts)}")

for post in posts:
    print(f"  [{post['id']}] {post['title']}")
