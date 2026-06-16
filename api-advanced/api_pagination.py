# Pagination - Looping through all pages of a paged API response
# Start the server first: python api-advanced/flask_server_advanced.py
import requests

BASE_URL = "http://localhost:5001"

# --- Fetch a single page ---
r = requests.get(f"{BASE_URL}/items", params={"page": 1, "per_page": 10})
page_data = r.json()
print(f"Page 1 of {page_data['total_pages']} — items: {len(page_data['items'])}")
print(f"Total items: {page_data['total']}")
print(f"Has next page: {page_data['has_next']}")

print()

# --- Collect ALL items across all pages automatically ---
all_items = []
page = 1

while True:
    r = requests.get(f"{BASE_URL}/items", params={"page": page, "per_page": 10})
    r.raise_for_status()
    data = r.json()

    all_items.extend(data["items"])
    print(f"Fetched page {data['page']}/{data['total_pages']} — "
          f"running total: {len(all_items)}")

    if not data["has_next"]:
        break
    page += 1

print(f"\nAll done — collected {len(all_items)} items total")
print("First :", all_items[0])
print("Last  :", all_items[-1])
