![Python Tinitiate Image](python_tinitiate.png)

# Python Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](../../README.md)

# Python API — Performance Tuning
* Default `requests` usage is fine for scripts making a handful of calls.
* When you need to make hundreds or thousands of requests, small inefficiencies compound.
* This section shows concrete techniques to measure and improve throughput and latency.

Topics covered:
- Why performance matters (TCP handshake cost)
- Connection pooling with Session
- Concurrent requests with ThreadPoolExecutor
- Fully async requests with `httpx`
- Response caching to eliminate redundant calls
- Gzip compression to reduce transfer size
- Streaming large downloads to save memory
- HTTPAdapter tuning (pool size, retries, default timeout)
- Benchmarking to measure the impact of each technique

## Setup

Install all dependencies for this section:
```
pip install requests httpx requests-cache
```

Start the basic server (used by most examples):
```
python api/flask_server.py
```

Start the advanced server (used by streaming download example):
```
python api-advanced/flask_server_advanced.py
```

---

## Why Performance Matters — The TCP Handshake Cost
* Every HTTP request without a persistent connection goes through:
  1. DNS lookup
  2. TCP three-way handshake (SYN → SYN-ACK → ACK)
  3. TLS handshake (for HTTPS — 2 more round trips)
  4. Send request → receive response
  5. Close connection
* Steps 1–3 add 50–200ms overhead **before any data is sent**.
* The key strategies below eliminate or amortize that overhead.

| Strategy | What it saves | When to use |
|---|---|---|
| Session (connection pooling) | Handshake per request | Always |
| Concurrent threads | Idle wait time | Multiple independent calls |
| Async (httpx) | Thread overhead | Very high concurrency |
| Caching | Entire round trip | Repeated reads of slow-changing data |
| Compression | Transfer bytes | Large JSON or text responses |
| Streaming | Memory usage | Large file / chunked responses |

---

## Connection Pooling with Session
* Without a Session, `requests` opens and closes a new TCP connection for every call.
* A Session reuses the same connections from a pool — eliminating the handshake cost on calls 2, 3, 4 …
* **Rule:** whenever you make more than one request to the same host, use a Session.

> **Client file:** [perf_connection_pooling.py](api-performance-tuning/perf_connection_pooling.py)
```python
import requests
import time

BASE_URL = "http://localhost:5000"
CALLS    = 10

# Without Session — new TCP connection every request
start = time.perf_counter()
for _ in range(CALLS):
    requests.get(f"{BASE_URL}/posts/1")
no_session_time = time.perf_counter() - start
print(f"No session  — {CALLS} requests: {no_session_time:.3f}s")

# With Session — connections reused from the pool
session = requests.Session()
start = time.perf_counter()
for _ in range(CALLS):
    session.get(f"{BASE_URL}/posts/1")
session_time = time.perf_counter() - start
session.close()
print(f"With session — {CALLS} requests: {session_time:.3f}s")
```

---

## Concurrent Requests — ThreadPoolExecutor
* Sequential requests wait for each response before sending the next — the server is idle while you wait.
* Threads let you send multiple requests at the same time and collect all the responses together.
* This is the biggest single speedup for making several independent calls.

> **Client file:** [perf_concurrent_threads.py](api-performance-tuning/perf_concurrent_threads.py)
```python
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:5000"
POST_IDS = list(range(1, 5))

session = requests.Session()

def fetch_post(post_id):
    r = session.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    r.raise_for_status()
    return r.json()

# Sequential
start = time.perf_counter()
sequential = [fetch_post(pid) for pid in POST_IDS]
print(f"Sequential : {time.perf_counter() - start:.3f}s")

# Concurrent (4 threads)
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(fetch_post, pid): pid for pid in POST_IDS}
    concurrent = [f.result() for f in as_completed(futures)]
print(f"Concurrent : {time.perf_counter() - start:.3f}s")

session.close()

# Use threads for I/O-bound work (network).
# Use multiprocessing for CPU-bound work (data crunching).
```

---

## Async Requests — httpx
* `httpx` is a drop-in replacement for `requests` that supports `async/await`.
* With `asyncio.gather()`, all requests fire simultaneously from a single thread — no thread overhead.
* Best for very high concurrency (hundreds of requests) or when you're already inside an async app.

> **Client file:** [perf_async_httpx.py](api-performance-tuning/perf_async_httpx.py)
```python
import httpx
import asyncio
import time

BASE_URL = "http://localhost:5000"
POST_IDS = list(range(1, 5))

async def fetch_post(client, post_id):
    r = await client.get(f"{BASE_URL}/posts/{post_id}")
    r.raise_for_status()
    return r.json()

async def fetch_all_sequential():
    async with httpx.AsyncClient() as client:
        return [await fetch_post(client, pid) for pid in POST_IDS]

async def fetch_all_concurrent():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_post(client, pid) for pid in POST_IDS]
        return await asyncio.gather(*tasks)   # all fire simultaneously

start = time.perf_counter()
results = asyncio.run(fetch_all_sequential())
print(f"Async sequential : {time.perf_counter() - start:.3f}s")

start = time.perf_counter()
results = asyncio.run(fetch_all_concurrent())
print(f"Async concurrent : {time.perf_counter() - start:.3f}s")

# httpx vs requests:
#   requests — synchronous, simpler, huge ecosystem
#   httpx    — sync AND async, HTTP/2 support, compatible API surface
```

---

## Response Caching
* If you call the same read-only endpoint repeatedly, you're paying network cost for the same data every time.
* `requests-cache` is a drop-in layer that stores responses and returns the cached copy until the TTL expires.

> **Client file:** [perf_caching.py](api-performance-tuning/perf_caching.py)
```python
import requests
import requests_cache
import time

BASE_URL = "http://localhost:5000"

cached_session = requests_cache.CachedSession(
    cache_name="api_cache",
    backend="memory",       # or "sqlite", "redis", "filesystem"
    expire_after=60,        # cache entries live for 60 seconds
)

for i in range(3):
    r = cached_session.get(f"{BASE_URL}/posts/1")
    source = "CACHE" if r.from_cache else "NETWORK"
    print(f"Call {i+1}: [{source}] status={r.status_code}")

# Force a fresh fetch ignoring the cache
r = cached_session.get(f"{BASE_URL}/posts/1", force_refresh=True)
print(f"Force-refreshed: from_cache={r.from_cache}")
cached_session.close()

# When to cache:  read-only data that changes slowly (config, lookup tables)
# When NOT to:    user-specific data, real-time feeds, write endpoints
```

---

## Gzip Compression
* Large JSON responses can be compressed by the server before sending, saving bandwidth.
* `requests` automatically adds `Accept-Encoding: gzip, deflate` to every request and decompresses the response for you — nothing to configure.
* This section shows how to verify it's working and how to opt out if needed.

> **Client file:** [perf_compression.py](api-performance-tuning/perf_compression.py)
```python
import requests

BASE_URL = "http://localhost:5000"

# requests already requests gzip compression automatically
r = requests.get(f"{BASE_URL}/posts")
print("Accept-Encoding sent     :", r.request.headers.get("Accept-Encoding"))
print("Content-Encoding received:", r.headers.get("Content-Encoding", "none"))
print("Decoded body size        :", len(r.content), "bytes")

# To opt out (rarely needed):
r2 = requests.get(f"{BASE_URL}/posts", headers={"Accept-Encoding": "identity"})
print("Uncompressed body size   :", len(r2.content), "bytes")

# Summary: leave the default — requests handles gzip negotiation automatically.
```

---

## Streaming Large Downloads
* Without `stream=True`, `requests` buffers the **entire** response in RAM before you can read a byte.
* With `stream=True`, the body arrives in chunks — you can process or write each chunk as it comes.
* Essential when the response could be larger than a few MB.

> **Client file:** [perf_streaming_download.py](api-performance-tuning/perf_streaming_download.py)
```python
import requests

BASE_URL = "http://localhost:5001"   # advanced server

# Stream a text response line by line
with requests.get(f"{BASE_URL}/stream?count=10", stream=True) as r:
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            print("Chunk:", line.decode())

# Stream a binary file to disk without loading it all into RAM
with requests.get(f"{BASE_URL}/response/binary", stream=True) as r:
    r.raise_for_status()
    with open("output.png", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
print("File saved.")

# Rule: use stream=True whenever downloading files
#       or when the response might exceed available RAM.
```

---

## HTTPAdapter Tuning — Pool Size and Default Timeout
* The default `HTTPAdapter` has `pool_maxsize=10` — meaning at most 10 simultaneous connections to one host.
* For high-throughput services, raise `pool_maxsize` to match your thread count.
* `requests` has no built-in "default timeout" — you must set one per request, or use the hook pattern below.

> **Client file:** [perf_adapter_tuning.py](api-performance-tuning/perf_adapter_tuning.py)
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://localhost:5000"

retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,               # wait 0.5s, 1s, 2s between retries
    status_forcelist=[429, 500, 503],
)

tuned_adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=4,               # connections to DIFFERENT hosts
    pool_maxsize=10,                  # connections to ONE host
)

session = requests.Session()
session.mount("http://",  tuned_adapter)
session.mount("https://", tuned_adapter)

# Inject a default timeout for every request through this session
DEFAULT_TIMEOUT   = (3, 10)           # (connect s, read s)
original_request  = session.request
def request_with_timeout(*args, **kwargs):
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    return original_request(*args, **kwargs)
session.request = request_with_timeout

r = session.get(f"{BASE_URL}/posts")
print(f"Status: {r.status_code}  Posts: {len(r.json())}")
session.close()
```

---

## Benchmarking — Measuring What Actually Helps
* Always measure before and after a change — assumed speedups can be wrong.
* The script below times four strategies side-by-side against the local server.

> **Client file:** [perf_benchmarking.py](api-performance-tuning/perf_benchmarking.py)
```python
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"
ROUNDS   = 10
URL      = f"{BASE_URL}/posts"

def benchmark(label, fn, rounds=ROUNDS):
    times = [time.perf_counter() - time.perf_counter() for _ in range(rounds)]  # warmup
    times = []
    for _ in range(rounds):
        start = time.perf_counter()
        fn()
        times.append(time.perf_counter() - start)
    avg = statistics.mean(times)
    print(f"{label:<35} avg={avg*1000:.1f}ms  median={statistics.median(times)*1000:.1f}ms")

_session = requests.Session()

def no_session():     requests.get(URL)
def with_session():   _session.get(URL)
def sequential_4():   [_session.get(f"{BASE_URL}/posts/{i}") for i in range(1,5)]
def concurrent_4():
    with ThreadPoolExecutor(max_workers=4) as ex:
        [f.result() for f in [ex.submit(_session.get, f"{BASE_URL}/posts/{i}") for i in range(1,5)]]

benchmark("1. No session (new conn each time) ", no_session)
benchmark("2. Persistent session              ", with_session)
benchmark("3. 4 posts sequential              ", sequential_4)
benchmark("4. 4 posts concurrent (4 threads)  ", concurrent_4)

_session.close()
```

---

##### [Back To Contents](../../README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
