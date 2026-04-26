from flask import Flask, jsonify, request, abort
from utils import fetch_product_from_api

app = Flask(__name__)

# In-memory database
inventory = [
    {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "ingredients_text": "Filtered water, almonds", "price": 4.99, "stock": 50},
    {"id": 2, "product_name": "Greek Yogurt", "brands": "Chobani", "ingredients_text": "Milk, cultures", "price": 1.50, "stock": 100}
]

def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)

def next_id():
    return inventory[-1]['id'] + 1 if inventory else 1

# --- CRUD ROUTES ---

# GET all items
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

# GET one item by id
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

# POST - add a new item manually
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.json
    if not data or 'product_name' not in data:
        abort(400, description="Missing product name")
    new_item = {
        "id": next_id(),
        "product_name": data.get("product_name"),
        "brands": data.get("brands", "Generic"),
        "ingredients_text": data.get("ingredients_text", "N/A"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

# PATCH - update price, stock, or product name
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    item['product_name'] = data.get('product_name', item['product_name'])
    item['price'] = data.get('price', item['price'])
    item['stock'] = data.get('stock', item['stock'])
    item['brands'] = data.get('brands', item['brands'])
    return jsonify(item), 200

# DELETE - remove an item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    inventory = [i for i in inventory if i['id'] != item_id]
    return jsonify({"result": True}), 200

# --- HELPER ROUTES ---

# SEARCH by product name
@app.route('/inventory/search', methods=['GET'])
def search_inventory():
    query = request.args.get('q', '').lower()
    results = [i for i in inventory if query in i['product_name'].lower()]
    return jsonify(results), 200

# FETCH from external API by barcode and add to inventory
@app.route('/inventory/fetch/<barcode>', methods=['POST'])
def fetch_and_add(barcode):
    product = fetch_product_from_api(barcode)
    if not product:
        return jsonify({"error": "Product not found in external API"}), 404
    data = request.json or {}
    new_item = {
        "id": next_id(),
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", "N/A"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

# LOW STOCK helper - items with stock below 10
@app.route('/inventory/low-stock', methods=['GET'])
def low_stock():
    results = [i for i in inventory if i['stock'] < 10]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
