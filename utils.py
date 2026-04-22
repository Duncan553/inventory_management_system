import requests

def fetch_product_from_api(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    headers = {"User-Agent": "InventoryApp - Education Project"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                p = data.get("product", {})
                return {
                    "product_name": p.get("product_name", "Unknown"),
                    "brands": p.get("brands", "Unknown"),
                    "ingredients_text": p.get("ingredients_text", "No data")
                }
    except Exception:
        return None
    return None
