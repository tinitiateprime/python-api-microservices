from flask import Flask, request, jsonify, Response, make_response
import xml.etree.ElementTree as ET
import time
import secrets

app = Flask(__name__)

# ---- In-memory state ----
rate_limit_hits = {}
valid_tokens = {}

RATE_LIMIT    = 3          # max requests per window
RATE_WINDOW   = 60         # seconds
CLIENT_ID     = "my-client-id"
CLIENT_SECRET = "my-client-secret"

ALL_ITEMS = [{"id": i, "value": f"item-{i}"} for i in range(1, 51)]  # 50 items for pagination


# ---- Response Types ----

@app.route("/response/json", methods=["GET"])
def response_json():
    return jsonify({"type": "json", "data": [1, 2, 3]})

@app.route("/response/text", methods=["GET"])
def response_text():
    return Response("Hello, this is a plain text response!", content_type="text/plain")

@app.route("/response/xml", methods=["GET"])
def response_xml():
    root = ET.Element("user")
    ET.SubElement(root, "id").text    = "1"
    ET.SubElement(root, "name").text  = "Alice"
    ET.SubElement(root, "email").text = "alice@example.com"
    return Response(ET.tostring(root, encoding="unicode"), content_type="application/xml")

@app.route("/response/binary", methods=["GET"])
def response_binary():
    # Minimal valid 1×1 white PNG
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
        b"\x00\x01\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return Response(png, content_type="image/png")


# ---- Form Data ----

@app.route("/form", methods=["POST"])
def handle_form():
    name  = request.form.get("name",  "")
    email = request.form.get("email", "")
    return jsonify({"received": {"name": name, "email": email}})


# ---- File Upload ----

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    f = request.files["file"]
    return jsonify({
        "filename":     f.filename,
        "content_type": f.content_type,
        "size_bytes":   len(f.read()),
    })


# ---- Pagination ----

@app.route("/items", methods=["GET"])
def get_items():
    page     = request.args.get("page",     1,  type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start    = (page - 1) * per_page
    end      = start + per_page
    total    = len(ALL_ITEMS)
    total_pages = (total + per_page - 1) // per_page
    return jsonify({
        "page":        page,
        "per_page":    per_page,
        "total":       total,
        "total_pages": total_pages,
        "has_next":    page < total_pages,
        "items":       ALL_ITEMS[start:end],
    })


# ---- Rate Limiting (3 requests per 60 s) ----

@app.route("/rate-limited", methods=["GET"])
def rate_limited():
    client_ip = request.remote_addr
    now  = time.time()
    hits = [t for t in rate_limit_hits.get(client_ip, []) if now - t < RATE_WINDOW]
    if len(hits) >= RATE_LIMIT:
        retry_after = int(RATE_WINDOW - (now - hits[0]))
        return jsonify({"error": "Too Many Requests"}), 429, {"Retry-After": str(retry_after)}
    hits.append(now)
    rate_limit_hits[client_ip] = hits
    return jsonify({"message": f"OK — hit {len(hits)}/{RATE_LIMIT} in this window"})


# ---- Cookies ----

@app.route("/set-cookie", methods=["GET"])
def set_cookie():
    resp = make_response(jsonify({"message": "Cookies set!"}))
    resp.set_cookie("session_id", "abc123",  max_age=300)
    resp.set_cookie("theme",      "dark",    max_age=300)
    return resp

@app.route("/check-cookie", methods=["GET"])
def check_cookie():
    session_id = request.cookies.get("session_id")
    theme      = request.cookies.get("theme")
    if not session_id:
        return jsonify({"error": "No session_id cookie — call /set-cookie first"}), 401
    return jsonify({"session_id": session_id, "theme": theme})


# ---- Streaming ----

@app.route("/stream", methods=["GET"])
def stream():
    count = request.args.get("count", 5, type=int)
    def generate():
        for i in range(1, count + 1):
            yield f"chunk {i} of {count}\n"
            time.sleep(0.1)
    return Response(generate(), content_type="text/plain")


# ---- API Versioning ----

@app.route("/v1/posts", methods=["GET"])
def v1_posts():
    return jsonify([
        {"id": 1, "title": "Post One"},
        {"id": 2, "title": "Post Two"},
    ])

@app.route("/v2/posts", methods=["GET"])
def v2_posts():
    return jsonify({
        "data": [
            {"id": 1, "title": "Post One", "author": "Alice", "published": "2024-01-01"},
            {"id": 2, "title": "Post Two", "author": "Bob",   "published": "2024-01-02"},
        ],
        "meta": {"total": 2, "version": "v2"},
    })


# ---- OAuth2 — Client Credentials simulation ----

@app.route("/token", methods=["POST"])
def get_token():
    data = request.get_json(force=True) if request.is_json else {}
    cid  = data.get("client_id")     or request.form.get("client_id")
    csec = data.get("client_secret") or request.form.get("client_secret")
    if cid != CLIENT_ID or csec != CLIENT_SECRET:
        return jsonify({"error": "invalid_client"}), 401
    token = secrets.token_hex(16)
    valid_tokens[token] = time.time() + 3600
    return jsonify({"access_token": token, "token_type": "Bearer", "expires_in": 3600})

@app.route("/v1/secure", methods=["GET"])
def secure_resource():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing Bearer token"}), 401
    token  = auth[7:]
    expiry = valid_tokens.get(token)
    if not expiry or time.time() > expiry:
        return jsonify({"error": "Token expired or invalid"}), 401
    return jsonify({"secret": "Secure resource accessed!", "token_prefix": token[:8] + "..."})


if __name__ == "__main__":
    print("Advanced API Server on http://localhost:5001")
    print(f"  OAuth2 client_id={CLIENT_ID}  client_secret={CLIENT_SECRET}")
    app.run(debug=True, port=5001)
