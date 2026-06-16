# HTTPAdapter Tuning - Control connection pool size, retries, and timeouts
# Start the basic server first: python api/flask_server.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://localhost:5000"

# ---- Default adapter has pool_connections=10, pool_maxsize=10 ----
# For a high-throughput service calling ONE host heavily, raise pool_maxsize
# to match your thread count so no thread waits for a free connection.

retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,               # wait 0.5s, 1s, 2s between retries
    status_forcelist=[429, 500, 503],
)

tuned_adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=4,               # connections to DIFFERENT hosts
    pool_maxsize=10,                  # connections to the SAME host
    pool_block=False,                 # don't block if pool is full — raise instead
)

session = requests.Session()
session.mount("http://",  tuned_adapter)
session.mount("https://", tuned_adapter)

# --- Default timeouts as a session-level hook ---
# requests has no built-in "default timeout" — use an event hook instead
DEFAULT_TIMEOUT = (3, 10)             # (connect seconds, read seconds)

original_request = session.request
def request_with_timeout(*args, **kwargs):
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    return original_request(*args, **kwargs)
session.request = request_with_timeout

# All requests now: auto-retry, tuned pool, and default timeout
r = session.get(f"{BASE_URL}/posts")
print(f"Status : {r.status_code}")
print(f"Posts  : {len(r.json())}")

session.close()
