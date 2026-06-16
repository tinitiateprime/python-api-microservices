# Response Caching - Avoid redundant API calls by caching responses
# Install: pip install requests-cache
# Start the basic server first: python api/flask_server.py
import requests
import requests_cache
import time

BASE_URL = "http://localhost:5000"

# ---- Without cache ----
session_no_cache = requests.Session()

start = time.perf_counter()
for _ in range(3):
    session_no_cache.get(f"{BASE_URL}/posts/1")
no_cache_time = time.perf_counter() - start
print(f"No cache — 3 requests: {no_cache_time:.3f}s (3 real network calls)")
session_no_cache.close()

# ---- With in-memory cache (60s TTL) ----
# The first call hits the network; subsequent calls return the cached response
cached_session = requests_cache.CachedSession(
    cache_name="api_cache",
    backend="memory",       # or "sqlite", "redis", "filesystem"
    expire_after=60,        # cache entries live for 60 seconds
)

start = time.perf_counter()
for i in range(3):
    r = cached_session.get(f"{BASE_URL}/posts/1")
    source = "CACHE" if r.from_cache else "NETWORK"
    print(f"  Call {i+1}: [{source}] status={r.status_code}")
cached_time = time.perf_counter() - start
print(f"With cache — 3 requests: {cached_time:.3f}s (only 1 real network call)")

# Force a fresh fetch (bypass the cache)
r = cached_session.get(f"{BASE_URL}/posts/1", force_refresh=True)
print(f"  Force-refreshed: from_cache={r.from_cache}")

cached_session.close()

# When to cache:
#   - Read-only data that doesn't change often (config, reference lists)
#   - Expensive aggregation endpoints
# When NOT to cache:
#   - User-specific data, real-time data, write endpoints
