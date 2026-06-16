# Compression - Request gzip-compressed responses to reduce transfer size
# Start the basic server first: python api/flask_server.py
# (requests already sends Accept-Encoding: gzip by default)
import requests

BASE_URL = "http://localhost:5000"

# --- requests enables gzip automatically ---
r = requests.get(f"{BASE_URL}/posts")
print("=== Default (gzip requested automatically) ===")
print("Accept-Encoding sent     :", r.request.headers.get("Accept-Encoding"))
print("Content-Encoding received:", r.headers.get("Content-Encoding", "none"))
print("Body size (after decode) :", len(r.content), "bytes")

# --- Disable automatic decompression (get raw compressed bytes) ---
# This is rarely needed — only if you want to store compressed bytes as-is
r_raw = requests.get(f"{BASE_URL}/posts", stream=True)
r_raw.raw.decode_content = False            # don't decompress
raw_bytes = r_raw.raw.read()
print("\n=== Raw (compressed) bytes ===")
print("Raw bytes read:", len(raw_bytes))

# --- Explicitly opt out of compression ---
r_no_enc = requests.get(
    f"{BASE_URL}/posts",
    headers={"Accept-Encoding": "identity"},   # request uncompressed
)
print("\n=== Uncompressed (identity) ===")
print("Accept-Encoding sent     :", r_no_enc.request.headers.get("Accept-Encoding"))
print("Body size                :", len(r_no_enc.content), "bytes")

# Summary: just leave the default — requests handles gzip negotiation automatically.
