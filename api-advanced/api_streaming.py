# Streaming Responses - Process large responses chunk by chunk without buffering all in memory
# Start the server first: python api-advanced/flask_server_advanced.py
import requests

BASE_URL = "http://localhost:5001"

# --- Stream=True: iterate over the response body as it arrives ---
# Without stream=True, requests downloads the entire body before giving it to you.
# With stream=True, you get chunks as they come — essential for large files.

print("=== Streaming text response ===")
with requests.get(f"{BASE_URL}/stream?count=8", stream=True) as r:
    r.raise_for_status()
    for chunk in r.iter_lines():          # one line at a time
        if chunk:
            print("Received:", chunk.decode("utf-8"))

# --- Stream a binary response (e.g., file download) ---
print("\n=== Streaming binary download ===")
total_bytes = 0
with requests.get(f"{BASE_URL}/response/binary", stream=True) as r:
    r.raise_for_status()
    for chunk in r.iter_content(chunk_size=1024):   # 1 KB at a time
        total_bytes += len(chunk)
        # In a real download you'd write chunk to a file:
        # f.write(chunk)

print(f"Downloaded {total_bytes} bytes total")
