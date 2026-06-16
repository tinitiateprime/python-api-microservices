# Error Handling - Checking Status Codes and Catching Exceptions
# Start the server first: python flask_server.py
import requests

BASE_URL = "http://localhost:5000"

# --- Check status code manually ---
response = requests.get(f"{BASE_URL}/posts/9999")
print("Status code :", response.status_code)       # 404
print("Error body  :", response.json())            # {'error': 'Post not found'}

print()

# --- Use raise_for_status() to auto-raise on 4xx/5xx ---
try:
    response = requests.get(f"{BASE_URL}/posts/9999")
    response.raise_for_status()
    print("Got data:", response.json())

except requests.exceptions.HTTPError as e:
    print(f"HTTP error     : {e}")                 # 404 Not Found

except requests.exceptions.ConnectionError:
    print("Could not connect to the server.")

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.RequestException as e:
    print(f"Something went wrong: {e}")
