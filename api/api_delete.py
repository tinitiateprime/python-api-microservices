# DELETE Request - Removing a Resource
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# Delete post with id=3
response = requests.delete(f"{BASE_URL}/posts/3")

print(response.status_code)        # 200
print(response.text)               # {}

# Confirm it is gone — GET should now return 404
check = requests.get(f"{BASE_URL}/posts/3")
print(check.status_code)           # 404
print(check.json())                # {'error': 'Post not found'}
