# Cookies - Setting and Reading Cookies Across Requests
# Start the server first: python api-advanced/flask_server_advanced.py
import requests

BASE_URL = "http://localhost:5001"

# ============================================================
# Approach 1: Manual — inspect and send cookies yourself
# ============================================================
print("=== Manual Cookie Handling ===")

# Step 1: GET /set-cookie — server sets cookies in the response
r = requests.get(f"{BASE_URL}/set-cookie")
print("Set-Cookie response:", r.status_code)
print("Cookies received   :", dict(r.cookies))   # {'session_id': 'abc123', 'theme': 'dark'}

# Step 2: Carry the cookies into the next request manually
r2 = requests.get(f"{BASE_URL}/check-cookie", cookies=r.cookies)
print("Check-cookie status:", r2.status_code)
print("Check-cookie result:", r2.json())

# ============================================================
# Approach 2: Session — cookies are carried automatically
# ============================================================
print("\n=== Session-Based Cookie Handling ===")

session = requests.Session()

# The session stores the Set-Cookie headers from each response
session.get(f"{BASE_URL}/set-cookie")
print("Cookies stored in session:", dict(session.cookies))

# Next request automatically includes those cookies
r3 = session.get(f"{BASE_URL}/check-cookie")
print("Auth check status  :", r3.status_code)
print("Auth check result  :", r3.json())

session.close()
