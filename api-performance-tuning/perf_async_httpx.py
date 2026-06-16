# Async Requests - Fully async HTTP using httpx (asyncio-native)
# Install: pip install httpx
# Start the basic server first: python api/flask_server.py
import httpx
import asyncio
import time

BASE_URL = "http://localhost:5000"
POST_IDS = list(range(1, 5))

async def fetch_post(client: httpx.AsyncClient, post_id: int) -> dict:
    r = await client.get(f"{BASE_URL}/posts/{post_id}")
    r.raise_for_status()
    return r.json()

async def fetch_all_sequential():
    async with httpx.AsyncClient() as client:
        results = []
        for pid in POST_IDS:
            results.append(await fetch_post(client, pid))
        return results

async def fetch_all_concurrent():
    async with httpx.AsyncClient() as client:
        tasks   = [fetch_post(client, pid) for pid in POST_IDS]
        results = await asyncio.gather(*tasks)    # all requests fire simultaneously
        return results

# ---- Run sequential async ----
start = time.perf_counter()
results = asyncio.run(fetch_all_sequential())
print(f"Async sequential : {time.perf_counter() - start:.3f}s — {len(results)} posts")

# ---- Run concurrent async ----
start = time.perf_counter()
results = asyncio.run(fetch_all_concurrent())
print(f"Async concurrent : {time.perf_counter() - start:.3f}s — {len(results)} posts")

for post in results:
    print(f"  [{post['id']}] {post['title']}")

# httpx vs requests:
#   requests — synchronous, simpler, huge ecosystem
#   httpx    — sync AND async, HTTP/2 support, mostly compatible API
