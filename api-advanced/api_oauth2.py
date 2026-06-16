# OAuth2 - Client Credentials Flow (machine-to-machine authentication)
# Start the server first: python api-advanced/flask_server_advanced.py
#
# Flow:
#   1. Exchange client_id + client_secret for an access token (POST /token)
#   2. Use the token as a Bearer token on subsequent requests
#   3. When the token expires, fetch a new one
import requests
import time

BASE_URL     = "http://localhost:5001"
CLIENT_ID     = "my-client-id"
CLIENT_SECRET = "my-client-secret"

# ---- Step 1: Get an access token ----
print("=== Step 1: Request access token ===")
r = requests.post(f"{BASE_URL}/token", json={
    "client_id":     CLIENT_ID,
    "client_secret": CLIENT_SECRET,
})
r.raise_for_status()
token_data   = r.json()
access_token = token_data["access_token"]
expires_in   = token_data["expires_in"]
print(f"Token (first 8): {access_token[:8]}...")
print(f"Expires in     : {expires_in}s")

# ---- Step 2: Use the token to access a protected resource ----
print("\n=== Step 2: Access secure endpoint ===")
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get(f"{BASE_URL}/v1/secure", headers=headers)
print(f"Status  : {r.status_code}")
print(f"Response: {r.json()}")

# ---- Step 3: What happens with a bad/expired token ----
print("\n=== Step 3: Bad token → 401 ===")
bad_headers = {"Authorization": "Bearer totally-fake-token"}
r = requests.get(f"{BASE_URL}/v1/secure", headers=bad_headers)
print(f"Status  : {r.status_code}")
print(f"Response: {r.json()}")

# ---- Helper: simple token manager (re-fetches when expired) ----
class TokenManager:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url     = token_url
        self.client_id     = client_id
        self.client_secret = client_secret
        self._token        = None
        self._expiry       = 0

    def get_token(self):
        if not self._token or time.time() >= self._expiry - 60:
            r = requests.post(self.token_url, json={
                "client_id":     self.client_id,
                "client_secret": self.client_secret,
            })
            r.raise_for_status()
            data = r.json()
            self._token  = data["access_token"]
            self._expiry = time.time() + data["expires_in"]
        return self._token

tm = TokenManager(f"{BASE_URL}/token", CLIENT_ID, CLIENT_SECRET)
print("\n=== TokenManager demo ===")
print("Token:", tm.get_token()[:8], "...")
