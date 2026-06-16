![Python Tinitiate Image](python_tinitiate.png)

# Python API Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](../../README.md)

# Python API
* An **API (Application Programming Interface)** is a way for two programs to talk to each other over a network.
* The most common type is a **REST API**, which uses **HTTP** — the same protocol your browser uses to load websites.
* Python makes it easy to both **call** (consume) APIs and **build** (create) them.

Key concepts:
- **Client**: the program that *sends* a request (e.g., your Python script)
- **Server**: the program that *receives* the request and sends back a response
- **Endpoint**: a URL that represents a specific resource or action (e.g., `http://localhost:5000/posts`)
- **HTTP Method**: the type of action — GET, POST, PUT, DELETE, PATCH
- **Status Code**: a number the server sends back to say whether the request worked (e.g., `200 OK`, `404 Not Found`)
- **JSON**: the most common data format used by REST APIs — looks like a Python dictionary

---

## Setup — Install and Run the Local Server

Install the two libraries used across all examples:
```
pip install requests flask
```

Start the local test server in one terminal — keep it running while you try the client files:
```
python api/flask_server.py
```

The server runs on `http://localhost:5000` and provides all the endpoints used by the examples below.

> **Server file:** [flask_server.py](api/flask_server.py)

---

## HTTP Methods
* HTTP methods tell the server **what action** you want to perform on a resource.

| Method | Purpose | Example Use |
|--------|---------|-------------|
| `GET` | Read / fetch data | Get a list of posts |
| `POST` | Create new data | Add a new post |
| `PUT` | Replace existing data entirely | Update all fields of a post |
| `PATCH` | Partially update existing data | Update only the title of a post |
| `DELETE` | Remove data | Delete a post |

---

## HTTP Status Codes
* The server always replies with a **status code** to tell you what happened.

| Code | Meaning | When you see it |
|------|---------|-----------------|
| `200` | OK | Request succeeded |
| `201` | Created | POST succeeded, new resource created |
| `204` | No Content | DELETE succeeded, nothing to return |
| `400` | Bad Request | You sent invalid data |
| `401` | Unauthorized | Missing or wrong authentication |
| `403` | Forbidden | Authenticated but not allowed |
| `404` | Not Found | The resource doesn't exist |
| `500` | Internal Server Error | Something broke on the server side |

---

## GET Request — Fetching a Single Resource
* A `GET` request retrieves one item from the server by its ID.
* The server returns the item in the **response body** as JSON.
* Use `response.json()` to convert the JSON text into a Python dictionary.

> **Client file:** [api_get_single.py](api/api_get_single.py)
```python
import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/posts/1")

print(response.status_code)        # 200

post = response.json()
print(post["id"])                   # 1
print(post["title"])                # Hello World
print(post["body"])                 # My first post
print(post["userId"])               # 1
```

---

## GET Request — Fetching a List
* When the endpoint returns multiple items, `response.json()` gives you a Python **list**.
* Iterate over it to access each item.

> **Client file:** [api_get_list.py](api/api_get_list.py)
```python
import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/posts")

print(response.status_code)        # 200

posts = response.json()            # list of dicts
print(f"Total posts: {len(posts)}")

for post in posts:
    print(f"  [{post['id']}] {post['title']}")
```

---

## Query Parameters — Filtering Results
* **Query parameters** are key-value pairs added to the URL after a `?` to filter or control what the server returns.
* Pass them as a `params` dictionary — `requests` builds the URL for you.

> **Client file:** [api_get_query_params.py](api/api_get_query_params.py)
```python
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
```

---

## Response Object — What You Get Back
* Every `requests` call returns a **Response object** with several useful attributes.
* You don't need all of them every time — but knowing they exist is handy for debugging.

> **Client file:** [api_response_object.py](api/api_response_object.py)
```python
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
```

---

## POST Request — Creating Data
* A `POST` request **sends data** to the server to create a new resource.
* Pass your data as a Python dict to the `json=` argument — `requests` serializes it to JSON automatically.
* A successful create returns status `201 Created`.

> **Client file:** [api_post.py](api/api_post.py)
```python
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
```

---

## PUT Request — Replacing Data
* A `PUT` request **replaces** an existing resource entirely.
* You must send the full updated object — any field you omit gets wiped.

> **Client file:** [api_put.py](api/api_put.py)
```python
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
```

---

## PATCH Request — Partially Updating Data
* A `PATCH` request updates **only the fields you send** — it leaves the rest unchanged.
* Use it when you want to change one field without resending the entire object.

> **Client file:** [api_patch.py](api/api_patch.py)
```python
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
```

---

## DELETE Request — Removing Data
* A `DELETE` request removes a resource from the server.
* The server usually returns `200` with an empty body `{}`.
* Confirm deletion by doing a follow-up GET — it should return `404`.

> **Client file:** [api_delete.py](api/api_delete.py)
```python
import requests

BASE_URL = "http://localhost:5000"

response = requests.delete(f"{BASE_URL}/posts/3")

print(response.status_code)        # 200
print(response.text)               # {}

# Confirm it is gone — GET should now return 404
check = requests.get(f"{BASE_URL}/posts/3")
print(check.status_code)           # 404
print(check.json())                # {'error': 'Post not found'}
```

---

## Request Headers — Sending Metadata
* **Headers** are key-value pairs sent with every request that give the server extra information.
* Common headers: `Content-Type`, `Accept`, `Authorization`, `User-Agent`.
* Pass them as a dictionary to the `headers=` argument.
* The `/headers` endpoint echoes back everything the server received — useful for debugging.

> **Client file:** [api_headers.py](api/api_headers.py)
```python
import requests

BASE_URL = "http://localhost:5000"

headers = {
    "Accept":          "application/json",
    "User-Agent":      "MyPythonApp/1.0",
    "X-Custom-Header": "hello-from-client",
}

response = requests.get(f"{BASE_URL}/headers", headers=headers)

print(response.status_code)        # 200

received = response.json()
print("Accept          :", received.get("Accept"))
print("User-Agent      :", received.get("User-Agent"))
print("X-Custom-Header :", received.get("X-Custom-Header"))
```

---

## Authentication — API Key in Header
* Many APIs require an **API key** to prove who you are.
* The most common pattern is to pass it in the `Authorization` header as a **Bearer token**.
* The server checks the key and returns `401 Unauthorized` if it's missing or wrong.

> **Client file:** [api_auth_apikey.py](api/api_auth_apikey.py)
```python
import requests

BASE_URL = "http://localhost:5000"
API_KEY = "secret-key-123"         # must match flask_server.py

# --- Without the key --- should get 401
r = requests.get(f"{BASE_URL}/protected")
print("Without key:", r.status_code, r.json())     # 401 Unauthorized

# --- With the correct key --- should get 200
headers = {"Authorization": f"Bearer {API_KEY}"}
r = requests.get(f"{BASE_URL}/protected", headers=headers)
print("With key   :", r.status_code, r.json())     # 200 + secret data
```

---

## Authentication — Basic Auth
* **Basic Auth** sends a username and password directly with the request.
* Pass a `(username, password)` tuple to the `auth=` argument — `requests` encodes it automatically.

> **Client file:** [api_auth_basic.py](api/api_auth_basic.py)
```python
import requests

BASE_URL = "http://localhost:5000"
USERNAME = "alice"
PASSWORD = "password123"

# --- Without credentials --- should get 401
r = requests.get(f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}")
print("Without auth:", r.status_code)              # 401

# --- With correct credentials --- should get 200
r = requests.get(
    f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}",
    auth=(USERNAME, PASSWORD)
)
print("With auth   :", r.status_code)              # 200
data = r.json()
print("Authenticated:", data["authenticated"])     # True
print("User        :", data["user"])               # alice
```

---

## Error Handling — Checking Status Codes
* Never assume a request succeeded — always check the status code.
* `response.raise_for_status()` raises an `HTTPError` automatically if the status is 4xx or 5xx.
* Wrap requests in `try/except` to handle network errors gracefully.

> **Client file:** [api_error_handling.py](api/api_error_handling.py)
```python
import requests

BASE_URL = "http://localhost:5000"

# --- Check status code manually ---
response = requests.get(f"{BASE_URL}/posts/9999")
print("Status code :", response.status_code)       # 404
print("Error body  :", response.json())

# --- Use raise_for_status() to auto-raise on 4xx/5xx ---
try:
    response = requests.get(f"{BASE_URL}/posts/9999")
    response.raise_for_status()
    print("Got data:", response.json())

except requests.exceptions.HTTPError as e:
    print(f"HTTP error     : {e}")                 # 404 Not Found

except requests.exceptions.ConnectionError:
    print("Could not connect to the server.")

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.RequestException as e:
    print(f"Something went wrong: {e}")
```

---

## Timeout — Preventing Hanging Requests
* By default, `requests` waits **forever** if the server doesn't respond.
* Always set a `timeout` (in seconds) so your program doesn't hang.
* The `/slow` endpoint in the test server sleeps for 8 seconds — perfect for seeing a timeout fire.

> **Client file:** [api_timeout.py](api/api_timeout.py)
```python
import requests

BASE_URL = "http://localhost:5000"

# --- Normal request with timeout (succeeds) ---
try:
    response = requests.get(f"{BASE_URL}/posts/1", timeout=5)
    print("Normal request:", response.status_code)    # 200

except requests.exceptions.Timeout:
    print("Normal request timed out.")

# --- Slow endpoint with a short timeout (times out) ---
try:
    response = requests.get(
        f"{BASE_URL}/slow",
        timeout=3                  # server takes 8s; we give it 3s
    )
    print("Slow request:", response.json())

except requests.exceptions.Timeout:
    print("Slow request timed out as expected!")      # this will print
```

---

## Working with JSON — Sending and Receiving
* JSON is just text that looks like a Python dict. Python's built-in `json` module converts between them.
* With `requests`, `response.json()` and `json=data` handle this automatically in most cases.

> **Client file:** [api_json.py](api/api_json.py)
```python
import requests
import json

BASE_URL = "http://localhost:5000"

# --- Receiving JSON ---
response = requests.get(f"{BASE_URL}/users/1")
user = response.json()              # converts JSON text → Python dict
print("type :", type(user))         # <class 'dict'>
print("name :", user["name"])
print("email:", user["email"])

# --- Sending JSON with json= argument (recommended) ---
payload = {"title": "JSON Post", "body": "Sent via json= arg", "userId": 1}
r = requests.post(f"{BASE_URL}/posts", json=payload)
print("\nPOST with json= :", r.status_code, "id:", r.json()["id"])

# --- Sending JSON manually (json.dumps + Content-Type header) ---
raw = json.dumps({"title": "Manual JSON", "body": "Sent manually", "userId": 2})
r = requests.post(
    f"{BASE_URL}/posts",
    data=raw,
    headers={"Content-Type": "application/json"},
)
print("POST manual     :", r.status_code, "id:", r.json()["id"])

# --- Pretty-printing a JSON response ---
data = r.json()
print("\nPretty-printed:")
print(json.dumps(data, indent=2))
```

---

## Session — Reusing Connections and Headers
* A `Session` object lets you **persist settings** (like headers or auth) across multiple requests.
* It also reuses the underlying TCP connection, which is faster when making many requests to the same server.

> **Client file:** [api_session.py](api/api_session.py)
```python
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
```

---

## HTTP vs HTTPS
* **HTTP** — data is sent as plain text; anyone who intercepts it can read it.
* **HTTPS** — data is **encrypted** using TLS/SSL before it is sent.
* Always use HTTPS for real APIs, especially when sending passwords, API keys, or personal data.
* `requests` verifies the server's SSL certificate by default. You can disable this, but never do so in production.

> **Client file:** [api_http_https.py](api/api_http_https.py)
```python
import requests

# --- HTTPS (secure) — certificate verified by default ---
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print("HTTPS status:", response.status_code)       # 200
print("Encrypted   : yes — TLS certificate verified automatically")

# --- Disable SSL verification (only for trusted internal servers) ---
# WARNING: never use verify=False against public internet endpoints
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1",
    verify=False
)
print("verify=False:", response.status_code)       # 200 but insecure
```

---

## Complete Example — CRUD Workflow
* A full create → read → replace → partial update → delete sequence in one script.
* Run this after starting the server to see all five HTTP methods working together.

> **Client file:** [api_crud_workflow.py](api/api_crud_workflow.py)
```python
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

# ---- 4. PARTIAL UPDATE (PATCH) ----
print("\n=== 4. PARTIAL UPDATE (PATCH) ===")
r = requests.patch(f"{BASE_URL}/posts/{post_id}", json={"title": "Patched Title Only"})
print(f"Status : {r.status_code}")                 # 200
print(f"Title  : {r.json()['title']}")
print(f"Body   : {r.json()['body']}")              # body from PUT still intact

# ---- 5. DELETE ----
print("\n=== 5. DELETE ===")
r = requests.delete(f"{BASE_URL}/posts/{post_id}")
print(f"Status : {r.status_code}")                 # 200

# ---- 6. VERIFY DELETED ----
print("\n=== 6. VERIFY DELETED (GET → 404) ===")
r = requests.get(f"{BASE_URL}/posts/{post_id}")
print(f"Status : {r.status_code}")                 # 404
print(f"Error  : {r.json()['error']}")
```

---

##### [Back To Contents](../../README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
