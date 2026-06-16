# GET Request - Fetching a Single Resource
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/posts/1")

print(response.status_code)        # 200

post = response.json()
print(post["id"])                   # 1
print(post["title"])                # Hello World
print(post["body"])                 # My first post
print(post["userId"])               # 1
