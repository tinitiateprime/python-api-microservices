# Connection Pooling - Session reuses TCP connections instead of opening a new one each time
# Start the basic server first: python api/flask_server.py
import requests
import time

BASE_URL = "http://localhost:5000"
CALLS    = 10

# ---- Without Session (new connection per request) ----
start = time.perf_counter()
for _ in range(CALLS):
    requests.get(f"{BASE_URL}/posts/1")
no_session_time = time.perf_counter() - start
print(f"No session  — {CALLS} requests: {no_session_time:.3f}s")

# ---- With Session (connections reused from the pool) ----
session = requests.Session()
start = time.perf_counter()
for _ in range(CALLS):
    session.get(f"{BASE_URL}/posts/1")
session_time = time.perf_counter() - start
session.close()
print(f"With session — {CALLS} requests: {session_time:.3f}s")

improvement = ((no_session_time - session_time) / no_session_time) * 100
print(f"Session was ~{improvement:.0f}% faster")

# Rule: whenever you make more than one request to the same host, use a Session.
