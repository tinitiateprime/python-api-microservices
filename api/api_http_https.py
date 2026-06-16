# HTTP vs HTTPS - Plain Text vs Encrypted Connections
# No local server needed — this example uses a public HTTPS test endpoint
import requests

# --- HTTPS (secure) — certificate verified by default ---
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print("HTTPS status:", response.status_code)       # 200
print("Encrypted   : yes — TLS certificate verified automatically")

# --- Disable SSL verification (only for trusted internal servers) ---
# WARNING: never disable verify=False against public internet endpoints
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1",
    verify=False                   # skips certificate check
)
print("verify=False:", response.status_code)       # 200 but insecure

# Key rule: always use HTTPS; never set verify=False in production code
