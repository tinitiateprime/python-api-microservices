# Rate Limiting and Retry - Handling 429 Too Many Requests gracefully
# Start the server first: python api-advanced/flask_server_advanced.py
# The /rate-limited endpoint allows only 3 requests per 60 seconds
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
            print(f"  Attempt {attempt}: 429 Too Many Requests — "
                  f"waiting {retry_after}s (Retry-After header)")
            time.sleep(retry_after)

        else:
            r.raise_for_status()

    raise RuntimeError(f"Failed after {max_retries} retries")


# Hit the endpoint several times — the 4th call will get a 429
print("Making 5 requests to the rate-limited endpoint:")
for i in range(1, 6):
    print(f"\nRequest {i}:")
    try:
        call_with_retry(f"{BASE_URL}/rate-limited", max_retries=3)
    except RuntimeError as e:
        print(f"  Gave up: {e}")
