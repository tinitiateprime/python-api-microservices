from flask import Flask, request, jsonify
import functools
import time

app = Flask(__name__)

# In-memory data store — resets each time the server restarts
posts = [
    {"id": 1, "title": "Hello World",  "body": "My first post",   "userId": 1},
    {"id": 2, "title": "Second Post",  "body": "My second post",  "userId": 1},
    {"id": 3, "title": "Third Post",   "body": "My third post",   "userId": 2},
    {"id": 4, "title": "Fourth Post",  "body": "My fourth post",  "userId": 2},
]
users = [
    {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "username": "alice"},
    {"id": 2, "name": "Bob Jones",   "email": "bob@example.com",   "username": "bob"},
]
next_post_id = 5
API_KEY = "secret-key-123"


# ---- Auth decorator ----
def require_api_key(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or auth[7:] != API_KEY:
            return jsonify({"error": "Unauthorized — send: Authorization: Bearer secret-key-123"}), 401
        return f(*args, **kwargs)
    return wrapper


# ---- Posts endpoints ----

@app.route("/posts", methods=["GET"])
def get_posts():
    user_id = request.args.get("userId", type=int)
    result = [p for p in posts if p["userId"] == user_id] if user_id else posts
    return jsonify(result)

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    return (jsonify(post), 200) if post else (jsonify({"error": "Post not found"}), 404)

@app.route("/posts", methods=["POST"])
def create_post():
    global next_post_id
    data = request.get_json(force=True)
    new_post = {
        "id": next_post_id,
        "title": data.get("title", ""),
        "body":  data.get("body",  ""),
        "userId": data.get("userId", 0),
    }
    posts.append(new_post)
    next_post_id += 1
    return jsonify(new_post), 201

@app.route("/posts/<int:post_id>", methods=["PUT"])
def replace_post(post_id):
    data = request.get_json(force=True)
    for i, p in enumerate(posts):
        if p["id"] == post_id:
            posts[i] = {
                "id": post_id,
                "title":  data.get("title",  ""),
                "body":   data.get("body",   ""),
                "userId": data.get("userId", 0),
            }
            return jsonify(posts[i])
    return jsonify({"error": "Post not found"}), 404

@app.route("/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    data = request.get_json(force=True)
    for i, p in enumerate(posts):
        if p["id"] == post_id:
            posts[i] = {**p, **data, "id": post_id}
            return jsonify(posts[i])
    return jsonify({"error": "Post not found"}), 404

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts
    before = len(posts)
    posts = [p for p in posts if p["id"] != post_id]
    if len(posts) == before:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({}), 200


# ---- Users endpoints ----

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    return (jsonify(user), 200) if user else (jsonify({"error": "User not found"}), 404)


# ---- Protected endpoint (requires API key) ----

@app.route("/protected", methods=["GET"])
@require_api_key
def protected():
    return jsonify({"message": "Access granted!", "secret_data": [42, 99, 7]})


# ---- Basic auth endpoint ----

@app.route("/basic-auth/<expected_user>/<expected_pass>", methods=["GET"])
def basic_auth(expected_user, expected_pass):
    auth = request.authorization
    if not auth or auth.username != expected_user or auth.password != expected_pass:
        return jsonify({"authenticated": False}), 401
    return jsonify({"authenticated": True, "user": auth.username})


# ---- Echo headers (shows what headers the server received) ----

@app.route("/headers", methods=["GET"])
def echo_headers():
    return jsonify(dict(request.headers))


# ---- Slow endpoint (sleeps 8s — used to demo timeout) ----

@app.route("/slow", methods=["GET"])
def slow():
    time.sleep(8)
    return jsonify({"message": "Finally done after 8 seconds!"})


if __name__ == "__main__":
    print(f"API Key for /protected : {API_KEY}")
    print("Endpoints:")
    print("  GET    /posts")
    print("  GET    /posts/<id>")
    print("  POST   /posts")
    print("  PUT    /posts/<id>")
    print("  PATCH  /posts/<id>")
    print("  DELETE /posts/<id>")
    print("  GET    /users")
    print("  GET    /users/<id>")
    print("  GET    /protected        (Bearer token required)")
    print("  GET    /basic-auth/<user>/<pass>")
    print("  GET    /headers")
    print("  GET    /slow             (8s delay — for timeout demo)")
    app.run(debug=True, port=5000)
