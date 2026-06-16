# Streaming Downloads - Download large responses without loading everything into RAM
# Start the advanced server first: python api-advanced/flask_server_advanced.py
import requests
import time

BASE_URL = "http://localhost:5001"

# ---- Without streaming — full response loaded into memory at once ----
print("=== Without stream=True ===")
start = time.perf_counter()
r = requests.get(f"{BASE_URL}/stream?count=10")
r.raise_for_status()
all_text = r.text           # entire body already in memory
elapsed = time.perf_counter() - start
print(f"Time    : {elapsed:.3f}s")
print(f"Size    : {len(all_text)} chars")
print(f"Content : {all_text[:60]}...")

# ---- With streaming — process each line as it arrives ----
print("\n=== With stream=True ===")
start = time.perf_counter()
chunks_received = 0

with requests.get(f"{BASE_URL}/stream?count=10", stream=True) as r:
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            chunks_received += 1
            print(f"  Received: {line.decode()}")

elapsed = time.perf_counter() - start
print(f"Time    : {elapsed:.3f}s")
print(f"Chunks  : {chunks_received}")

# ---- Streaming a file download to disk ----
print("\n=== Stream binary to disk ===")
OUTPUT_FILE = "downloaded.png"
with requests.get(f"{BASE_URL}/response/binary", stream=True) as r:
    r.raise_for_status()
    with open(OUTPUT_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
print(f"Saved to {OUTPUT_FILE}")

# Rule: always use stream=True when downloading files or when the response
# could be larger than a few MB.
