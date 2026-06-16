# Timeout - Preventing Your Program from Hanging Forever
# Start the server first: python flask_server.py
# The /slow endpoint sleeps for 8 seconds — our 3s timeout will fire first
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
