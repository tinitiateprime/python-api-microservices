# Form Data vs JSON - Two ways to send data in a POST request
# Start the server first: python api-advanced/flask_server_advanced.py
import requests

BASE_URL = "http://localhost:5001"

# --- Form-encoded data (data=) ---
# Content-Type becomes: application/x-www-form-urlencoded
# Used by HTML forms and some older APIs
form_payload = {
    "name":  "Alice",
    "email": "alice@example.com",
}
r = requests.post(f"{BASE_URL}/form", data=form_payload)
print("=== Form-encoded (data=) ===")
print("Status :", r.status_code)
print("Sent as: application/x-www-form-urlencoded")
print("Result :", r.json())

# --- JSON data (json=) ---
# Content-Type becomes: application/json
# Used by modern REST APIs
json_payload = {
    "name":  "Bob",
    "email": "bob@example.com",
}
# Note: /form reads request.form, so json= won't be parsed there.
# This example just shows the difference in how the data is sent.
print("\n=== JSON (json=) ===")
r2 = requests.post("http://localhost:5001/form", data=json_payload)
print("Status :", r2.status_code)
print("Content-Type sent: application/x-www-form-urlencoded")
print("Result :", r2.json())

# Key rule:
#   data=dict  → form-encoded  (server reads request.form)
#   json=dict  → JSON body     (server reads request.json or request.get_json())
