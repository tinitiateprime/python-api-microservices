# Retry Adapter - Automatic retries with exponential backoff using HTTPAdapter
# Start the server first: python api-advanced/flask_server_advanced.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://localhost:5001"

# --- Configure retry behavior ---
retry_strategy = Retry(
    total=4,                          # total number of retries
    backoff_factor=1,                 # wait 1s, 2s, 4s, 8s between retries
    status_forcelist=[429, 500, 502,  # retry on these HTTP status codes
                      503, 504],
    allowed_methods=["GET", "POST"],  # only retry these methods
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("http://",  adapter)
session.mount("https://", adapter)

# Now every request through this session automatically retries on failure
print("Making request with auto-retry adapter...")
try:
    r = session.get(f"{BASE_URL}/items?page=1&per_page=5", timeout=10)
    r.raise_for_status()
    data = r.json()
    print(f"Status   : {r.status_code}")
    print(f"Items    : {len(data['items'])}")
    print(f"Total    : {data['total']}")
except requests.exceptions.RetryError as e:
    print(f"All retries exhausted: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
finally:
    session.close()
