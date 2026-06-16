# Concurrent Requests - Fetch multiple URLs in parallel using ThreadPoolExecutor
# Start the basic server first: python api/flask_server.py
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:5000"
POST_IDS = list(range(1, 5))            # fetch posts 1–4

session = requests.Session()

def fetch_post(post_id):
    r = session.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    r.raise_for_status()
    return r.json()

# ---- Sequential ----
start = time.perf_counter()
sequential_results = [fetch_post(pid) for pid in POST_IDS]
seq_time = time.perf_counter() - start
print(f"Sequential : {seq_time:.3f}s — fetched {len(sequential_results)} posts")

# ---- Concurrent (4 threads) ----
start = time.perf_counter()
concurrent_results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(fetch_post, pid): pid for pid in POST_IDS}
    for future in as_completed(futures):
        concurrent_results.append(future.result())
conc_time = time.perf_counter() - start
print(f"Concurrent : {conc_time:.3f}s — fetched {len(concurrent_results)} posts")

speedup = seq_time / conc_time if conc_time > 0 else 0
print(f"Speedup    : ~{speedup:.1f}x faster")

session.close()

# When to use threads:
#   - I/O-bound work (waiting for network responses) — threads help a lot
#   - CPU-bound work (number crunching) — use multiprocessing instead
