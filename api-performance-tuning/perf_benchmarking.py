# Benchmarking - Compare the performance of different request strategies
# Start the basic server first: python api/flask_server.py
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"
ROUNDS   = 10
URL      = f"{BASE_URL}/posts"

def benchmark(label, fn, rounds=ROUNDS):
    times = []
    for _ in range(rounds):
        start = time.perf_counter()
        fn()
        times.append(time.perf_counter() - start)
    avg = statistics.mean(times)
    med = statistics.median(times)
    print(f"{label:<35} avg={avg*1000:.1f}ms  median={med*1000:.1f}ms  "
          f"min={min(times)*1000:.1f}ms  max={max(times)*1000:.1f}ms")

# ---- 1. New session each request ----
def no_session():
    requests.get(URL)

# ---- 2. Persistent session ----
_session = requests.Session()
def with_session():
    _session.get(URL)

# ---- 3. Fetch 4 posts concurrently with threads ----
def concurrent_4():
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(_session.get, f"{BASE_URL}/posts/{i}") for i in range(1, 5)]
        [f.result() for f in futures]

# ---- 4. Fetch 4 posts sequentially ----
def sequential_4():
    for i in range(1, 5):
        _session.get(f"{BASE_URL}/posts/{i}")

print(f"Benchmarking {ROUNDS} rounds each against {BASE_URL}\n")
benchmark("1. No session (new conn each time) ", no_session)
benchmark("2. Persistent session              ", with_session)
benchmark("3. 4 posts sequential              ", sequential_4)
benchmark("4. 4 posts concurrent (4 threads)  ", concurrent_4)

_session.close()
