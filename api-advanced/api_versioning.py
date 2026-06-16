# API Versioning - Calling v1 vs v2 of the same endpoint
# Start the server first: python api-advanced/flask_server_advanced.py
import requests

BASE_URL = "http://localhost:5001"

# ---- Strategy 1: Version in the URL path (most common) ----
print("=== v1 /v1/posts ===")
r = requests.get(f"{BASE_URL}/v1/posts")
posts_v1 = r.json()                    # simple list
for p in posts_v1:
    print(f"  id={p['id']}  title={p['title']}")

print("\n=== v2 /v2/posts ===")
r = requests.get(f"{BASE_URL}/v2/posts")
payload_v2 = r.json()                  # dict with 'data' and 'meta'
for p in payload_v2["data"]:
    print(f"  id={p['id']}  title={p['title']}  author={p['author']}  published={p['published']}")
print("meta:", payload_v2["meta"])

# ---- Strategy 2: Version in a header (less common but valid) ----
# Some APIs use:  Accept: application/vnd.myapi.v2+json
# or:             API-Version: 2
r = requests.get(
    f"{BASE_URL}/v2/posts",
    headers={"API-Version": "2"}       # server would read this header
)
print("\n=== Header-versioned request ===")
print("Status:", r.status_code)

# Key takeaway:
#   v1 returns a plain list — simple but less info
#   v2 returns a richer envelope with metadata — more flexible for the client
