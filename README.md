![Python Tinitiate Image](python_tinitiate.png)

# Python API and Microsservices Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](../../README.md)

## [Python API](api.md)
* An **API (Application Programming Interface)** is a way for two programs to talk to each other over a network.
* The most common type is a **REST API**, which uses **HTTP** — the same protocol your browser uses to load websites.
* Python makes it easy to both **call** (consume) APIs and **build** (create) them.

Key concepts:
- **Client**: the program that *sends* a request (e.g., your Python script)
- **Server**: the program that *receives* the request and sends back a response
- **Endpoint**: a URL that represents a specific resource or action (e.g., `http://localhost:5000/posts`)
- **HTTP Method**: the type of action — GET, POST, PUT, DELETE, PATCH
- **Status Code**: a number the server sends back to say whether the request worked (e.g., `200 OK`, `404 Not Found`)
- **JSON**: the most common data format used by REST APIs — looks like a Python dictionary

---
## [Python API Advanced](api-advanced.md)
* Goes beyond basic GET/POST to cover real-world patterns every API client needs.
* Topics include:
  - Response types — JSON, plain text, XML, and binary (images, PDFs)
  - Sending form data vs JSON in a POST body
  - Uploading files with multipart/form-data
  - Paginating through large result sets automatically
  - Handling `429 Too Many Requests` with manual retry and `Retry-After`
  - Automatic retries with exponential backoff via `HTTPAdapter`
  - Reading and sending cookies; session-based cookie persistence
  - Streaming large responses chunk-by-chunk with `stream=True`
  - API versioning — calling `/v1` vs `/v2` endpoints
  - OAuth2 client credentials flow — exchanging a secret for a Bearer token

---
## [Python API Performance Tuning](api-performance-tuning.md)
* Covers techniques to reduce latency and increase throughput when making many API calls.
* Topics include:
  - Why TCP handshakes are expensive and how connection pooling eliminates the cost
  - Reusing connections with `Session` — the simplest and most effective speedup
  - Concurrent requests using `ThreadPoolExecutor` — fetch multiple endpoints in parallel
  - Fully async HTTP with `httpx` and `asyncio.gather()` for very high concurrency
  - Response caching with `requests-cache` to skip redundant network calls
  - Gzip compression — how `requests` negotiates it automatically and how to verify it
  - Streaming large downloads with `iter_content()` to avoid buffering in RAM
  - Tuning `HTTPAdapter` — pool size, retry strategy, and injecting a default timeout
  - Benchmarking — timing strategies side-by-side to measure what actually helps

##### [Back To Contents](../../README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
