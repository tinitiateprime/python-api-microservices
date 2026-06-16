# Complete CRUD Workflow - Create, Read, Update, Delete in sequence
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# ---- 1. CREATE (POST) ----
print("=== 1. CREATE (POST) ===")
new_post = {"title": "CRUD Tutorial", "body": "Learning CRUD with Python", "userId": 1}
r = requests.post(f"{BASE_URL}/posts", json=new_post)
print(f"Status : {r.status_code}")                 # 201
created = r.json()
post_id = created["id"]
print(f"ID     : {post_id}")
print(f"Title  : {created['title']}")

# ---- 2. READ (GET) ----
print("\n=== 2. READ (GET) ===")
r = requests.get(f"{BASE_URL}/posts/{post_id}")
print(f"Status : {r.status_code}")                 # 200
print(f"Title  : {r.json()['title']}")

# ---- 3. REPLACE (PUT) ----
print("\n=== 3. REPLACE (PUT) ===")
replaced = {"title": "Replaced Title", "body": "Completely new body", "userId": 2}
r = requests.put(f"{BASE_URL}/posts/{post_id}", json=replaced)
print(f"Status : {r.status_code}")                 # 200
print(f"Title  : {r.json()['title']}")
print(f"Body   : {r.json()['body']}")

# ---- 4. PARTIAL UPDATE (PATCH) ----
print("\n=== 4. PARTIAL UPDATE (PATCH) ===")
r = requests.patch(f"{BASE_URL}/posts/{post_id}", json={"title": "Patched Title Only"})
print(f"Status : {r.status_code}")                 # 200
print(f"Title  : {r.json()['title']}")             # Patched Title Only
print(f"Body   : {r.json()['body']}")              # body from PUT still intact

# ---- 5. DELETE ----
print("\n=== 5. DELETE ===")
r = requests.delete(f"{BASE_URL}/posts/{post_id}")
print(f"Status : {r.status_code}")                 # 200

# ---- 6. VERIFY IT IS GONE ----
print("\n=== 6. VERIFY DELETED (GET → 404) ===")
r = requests.get(f"{BASE_URL}/posts/{post_id}")
print(f"Status : {r.status_code}")                 # 404
print(f"Error  : {r.json()['error']}")
