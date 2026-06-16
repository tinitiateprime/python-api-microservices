![Python Tinitiate Image](python_tinitiate.png)

# Python Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](../../README.md)

# Python API — Advanced
* This section covers topics you need once you go beyond basic GET/POST calls.
* Prerequisites: complete [Python API](api.md) first.

Topics covered:
- Different response types (JSON, text, XML, binary)
- Sending form data vs JSON
- Uploading files
- Paginating through large result sets
- Handling rate limits and retrying failed requests
- Automatic retries with exponential backoff
- Working with cookies
- Streaming large responses
- API versioning (v1 vs v2)
- OAuth2 client credentials flow

## Setup — Install and Run the Advanced Server

Install dependencies:
```
pip install requests flask
```

Start the advanced test server in one terminal — keep it running while you try the client files:
```
python api-advanced/flask_server_advanced.py
```

The server runs on `http://localhost:5001`.

> **Server file:** [flask_server_advanced.py](api-advanced/flask_server_advanced.py)

---

## Response Types — JSON, Text, XML, Binary
* Not every API returns JSON. You need to read the `Content-Type` header to know how to parse the response.
* Use `.json()` for JSON, `.text` for strings, `.content` for raw bytes.

| Content-Type | How to read | When you see it |
|---|---|---|
| `application/json` | `r.json()` | REST APIs |
| `text/plain` | `r.text` | Simple status messages |
| `application/xml` | `r.text` + XML parser | Older enterprise APIs, RSS feeds |
| `image/png`, `application/pdf` | `r.content` | File downloads |

> **Client file:** [api_response_types.py](api-advanced/api_response_types.py)
```python
import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:5001"

# --- JSON response ---
r = requests.get(f"{BASE_URL}/response/json")
print("Content-Type:", r.headers["Content-Type"])
data = r.json()                           # parse directly to dict/list
print("data:", data)

# --- Plain text response ---
r = requests.get(f"{BASE_URL}/response/text")
print("text:", r.text)                    # use .text, not .json()

# --- XML response ---
r = requests.get(f"{BASE_URL}/response/xml")
root = ET.fromstring(r.text)
print("name :", root.find("name").text)

# --- Binary response (image, PDF, etc.) ---
r = requests.get(f"{BASE_URL}/response/binary")
print("size (bytes):", len(r.content))    # use .content for raw bytes
```

---

## Sending Form Data vs JSON
* There are two common ways to send data in a POST request — choose based on what the server expects.
* `data=dict` sends form-encoded data (like an HTML form).
* `json=dict` sends a JSON body (standard for REST APIs).

> **Client file:** [api_form_data.py](api-advanced/api_form_data.py)
```python
import requests

BASE_URL = "http://localhost:5001"

# --- Form-encoded (data=) ---
# Content-Type: application/x-www-form-urlencoded
form_payload = {"name": "Alice", "email": "alice@example.com"}
r = requests.post(f"{BASE_URL}/form", data=form_payload)
print("Form result:", r.json())

# --- JSON body (json=) ---
# Content-Type: application/json
json_payload = {"name": "Bob", "email": "bob@example.com"}
r = requests.post(f"{BASE_URL}/form", data=json_payload)
print("JSON result:", r.json())

# Key rule:
#   data=dict  → form-encoded  (server reads request.form)
#   json=dict  → JSON body     (server reads request.get_json())
```

---

## File Upload — Multipart Form Data
* Use the `files=` argument to upload a file. `requests` sets the `Content-Type: multipart/form-data` header automatically.
* Pass a `(filename, file-object, content-type)` tuple for full control.

> **Client file:** [api_file_upload.py](api-advanced/api_file_upload.py)
```python
import requests
import io

BASE_URL = "http://localhost:5001"

# --- Upload from memory (no real file needed) ---
fake_file = io.BytesIO(b"Hello, this is the file content!")

r = requests.post(
    f"{BASE_URL}/upload",
    files={"file": ("hello.txt", fake_file, "text/plain")}
    #           ^tuple: (filename, file-like object, content-type)
)

print("Status      :", r.status_code)     # 200
result = r.json()
print("Filename    :", result["filename"])
print("Size (bytes):", result["size_bytes"])

# --- Upload from disk ---
# with open("report.pdf", "rb") as f:
#     r = requests.post(f"{BASE_URL}/upload", files={"file": f})
```

---

## Pagination — Looping Through All Pages
* Most APIs that return lists use pagination to avoid returning thousands of items at once.
* Keep requesting the next page until the API tells you there are no more pages.

> **Client file:** [api_pagination.py](api-advanced/api_pagination.py)
```python
import requests

BASE_URL = "http://localhost:5001"

# --- Fetch a single page ---
r = requests.get(f"{BASE_URL}/items", params={"page": 1, "per_page": 10})
page_data = r.json()
print(f"Page 1 of {page_data['total_pages']} — items: {len(page_data['items'])}")
print(f"Has next page: {page_data['has_next']}")

# --- Collect ALL items across all pages automatically ---
all_items = []
page = 1

while True:
    r = requests.get(f"{BASE_URL}/items", params={"page": page, "per_page": 10})
    r.raise_for_status()
    data = r.json()

    all_items.extend(data["items"])
    print(f"Fetched page {data['page']}/{data['total_pages']}")

    if not data["has_next"]:
        break
    page += 1

print(f"Total items collected: {len(all_items)}")
```

---

## Rate Limiting and Manual Retry
* Many APIs cap how many requests you can make per minute and return `429 Too Many Requests`.
* When you get a 429, read the `Retry-After` header and wait that many seconds before trying again.

> **Client file:** [api_rate_limit_retry.py](api-advanced/api_rate_limit_retry.py)
```python
import requests
import time

BASE_URL = "http://localhost:5001"

def call_with_retry(url, max_retries=5):
    for attempt in range(1, max_retries + 1):
        r = requests.get(url)

        if r.status_code == 200:
            print(f"  Attempt {attempt}: OK — {r.json()['message']}")
            return r

        if r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 5))
            print(f"  Attempt {attempt}: 429 — waiting {retry_after}s")
            time.sleep(retry_after)

        else:
            r.raise_for_status()

    raise RuntimeError(f"Failed after {max_retries} retries")

call_with_retry(f"{BASE_URL}/rate-limited")
```

---

## Automatic Retry with HTTPAdapter
* Instead of writing manual retry loops, mount an `HTTPAdapter` with a `Retry` policy onto your session.
* The adapter automatically retries on the status codes you specify, with exponential backoff.

> **Client file:** [api_retry_adapter.py](api-advanced/api_retry_adapter.py)
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://localhost:5001"

retry_strategy = Retry(
    total=4,                          # total number of retries
    backoff_factor=1,                 # wait 1s, 2s, 4s, 8s between retries
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://",  adapter)
session.mount("https://", adapter)

try:
    r = session.get(f"{BASE_URL}/items?page=1&per_page=5", timeout=10)
    r.raise_for_status()
    print("Status:", r.status_code)
    print("Items :", len(r.json()["items"]))
except requests.exceptions.RetryError as e:
    print(f"All retries exhausted: {e}")
finally:
    session.close()
```

---

## Cookies — Setting and Reading
* Cookies are small key-value pairs the server sends to the client, and the client sends them back on every subsequent request.
* A `Session` carries cookies automatically. Without a Session, you manage them manually.

> **Client file:** [api_cookies.py](api-advanced/api_cookies.py)
```python
import requests

BASE_URL = "http://localhost:5001"

# --- Manual: inspect and forward cookies yourself ---
r = requests.get(f"{BASE_URL}/set-cookie")
print("Cookies received:", dict(r.cookies))   # {'session_id': 'abc123', 'theme': 'dark'}

r2 = requests.get(f"{BASE_URL}/check-cookie", cookies=r.cookies)
print("Auth check:", r2.json())

# --- Session: cookies carried automatically ---
session = requests.Session()
session.get(f"{BASE_URL}/set-cookie")               # stores the cookies
r3 = session.get(f"{BASE_URL}/check-cookie")        # sends them automatically
print("Session auth check:", r3.json())
session.close()
```

---

## Streaming Responses — Chunk-by-Chunk Processing
* By default, `requests` downloads the entire response body before you can read it.
* With `stream=True`, the body arrives in pieces — essential when the response could be large.
* Use `iter_lines()` for text streams and `iter_content(chunk_size=N)` for binary downloads.

> **Client file:** [api_streaming.py](api-advanced/api_streaming.py)
```python
import requests

BASE_URL = "http://localhost:5001"

# --- Stream a text response line by line ---
with requests.get(f"{BASE_URL}/stream?count=8", stream=True) as r:
    r.raise_for_status()
    for chunk in r.iter_lines():
        if chunk:
            print("Received:", chunk.decode("utf-8"))

# --- Stream a binary download to disk ---
OUTPUT_FILE = "downloaded.png"
with requests.get(f"{BASE_URL}/response/binary", stream=True) as r:
    r.raise_for_status()
    with open(OUTPUT_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
print(f"Saved to {OUTPUT_FILE}")
```

---

## API Versioning — Calling v1 vs v2
* APIs evolve over time. Versioning lets the server change its format without breaking existing clients.
* The most common strategy is putting the version number in the URL path (`/v1/`, `/v2/`).

> **Client file:** [api_versioning.py](api-advanced/api_versioning.py)
```python
import requests

BASE_URL = "http://localhost:5001"

# --- v1: returns a simple list ---
r = requests.get(f"{BASE_URL}/v1/posts")
posts_v1 = r.json()
for p in posts_v1:
    print(f"v1 — id={p['id']}  title={p['title']}")

# --- v2: returns a richer envelope with metadata ---
r = requests.get(f"{BASE_URL}/v2/posts")
payload_v2 = r.json()
for p in payload_v2["data"]:
    print(f"v2 — id={p['id']}  title={p['title']}  author={p['author']}")
print("meta:", payload_v2["meta"])

# Strategy 2: version in a request header (less common)
r = requests.get(f"{BASE_URL}/v2/posts", headers={"API-Version": "2"})
print("Header-versioned status:", r.status_code)
```

---

## OAuth2 — Client Credentials Flow
* OAuth2 is the standard for secure machine-to-machine API access.
* **Client Credentials** flow: exchange a client ID + secret for a short-lived access token, then use that token as a Bearer header.
* When the token expires, fetch a new one — the `TokenManager` class below handles this automatically.

> **Client file:** [api_oauth2.py](api-advanced/api_oauth2.py)
```python
import requests
import time

BASE_URL      = "http://localhost:5001"
CLIENT_ID     = "my-client-id"
CLIENT_SECRET = "my-client-secret"

# Step 1: Get an access token
r = requests.post(f"{BASE_URL}/token", json={
    "client_id":     CLIENT_ID,
    "client_secret": CLIENT_SECRET,
})
r.raise_for_status()
token_data   = r.json()
access_token = token_data["access_token"]
print(f"Token (first 8): {access_token[:8]}...")

# Step 2: Use the token
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get(f"{BASE_URL}/v1/secure", headers=headers)
print(f"Secure resource: {r.json()}")

# Step 3: Bad token → 401
r = requests.get(f"{BASE_URL}/v1/secure",
                 headers={"Authorization": "Bearer fake-token"})
print(f"Bad token: {r.status_code} {r.json()}")

# TokenManager — auto-refreshes when the token is close to expiring
class TokenManager:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url     = token_url
        self.client_id     = client_id
        self.client_secret = client_secret
        self._token        = None
        self._expiry       = 0

    def get_token(self):
        if not self._token or time.time() >= self._expiry - 60:
            r = requests.post(self.token_url, json={
                "client_id":     self.client_id,
                "client_secret": self.client_secret,
            })
            r.raise_for_status()
            data         = r.json()
            self._token  = data["access_token"]
            self._expiry = time.time() + data["expires_in"]
        return self._token

tm = TokenManager(f"{BASE_URL}/token", CLIENT_ID, CLIENT_SECRET)
print("Managed token:", tm.get_token()[:8], "...")
```

---

##### [Back To Contents](../../README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
