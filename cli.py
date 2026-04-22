import requests
from utils import fetch_product_from_api

URL = "http://127.0.0.1:5000/inventory"

def run_cli():
    while True:
        print("\n1. View All | 2. Add Item | 3. Import via Barcode | 4. Update | 5. Delete | 6. Exit")
        cmd = input("> ")
        
        if cmd == "1":
            print(requests.get(URL).json())
        elif cmd == "2":
            name = input("Name: ")
            price = float(input("Price: "))
            requests.post(URL, json={"product_name": name, "price": price})
        elif cmd == "3":
            bc = input("Barcode: ")
            ext = fetch_product_from_api(bc)
            if ext:
                print(f"Found: {ext['product_name']}")
                ext['price'] = float(input("Enter Price: "))
                ext['stock'] = int(input("Enter Stock: "))
                requests.post(URL, json=ext)
            else:
                print("Product not found.")
        elif cmd == "4":
            idx = input("Item ID: ")
            p = float(input("New Price: "))
            s = int(input("New Stock: "))
            requests.patch(f"{URL}/{idx}", json={"price": p, "stock": s})
        elif cmd == "5":
            idx = input("Item ID to Delete: ")
            requests.delete(f"{URL}/{idx}")
        elif cmd == "6":
            break

if __name__ == "__main__":
    run_cli()
