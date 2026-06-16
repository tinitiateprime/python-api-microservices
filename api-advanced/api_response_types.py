# Response Types - Handling JSON, Text, XML, and Binary Responses
# Start the server first: python api-advanced/flask_server_advanced.py
import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:5001"

# --- JSON response (most common) ---
r = requests.get(f"{BASE_URL}/response/json")
print("=== JSON ===")
print("Content-Type:", r.headers["Content-Type"])
data = r.json()                           # parse directly to dict/list
print("data:", data)

# --- Plain text response ---
r = requests.get(f"{BASE_URL}/response/text")
print("\n=== Text ===")
print("Content-Type:", r.headers["Content-Type"])
print("text:", r.text)                    # use .text, not .json()

# --- XML response ---
r = requests.get(f"{BASE_URL}/response/xml")
print("\n=== XML ===")
print("Content-Type:", r.headers["Content-Type"])
root = ET.fromstring(r.text)              # parse XML from the response text
print("name :", root.find("name").text)
print("email:", root.find("email").text)

# --- Binary response (image, PDF, etc.) ---
r = requests.get(f"{BASE_URL}/response/binary")
print("\n=== Binary ===")
print("Content-Type:", r.headers["Content-Type"])
print("size (bytes):", len(r.content))    # use .content for raw bytes
# Save to disk if needed:
# with open("image.png", "wb") as f:
#     f.write(r.content)
