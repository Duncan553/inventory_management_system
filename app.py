from flask import Flask, jsonify, request, abort
from utils import fetch_product_from_api

app = Flask(__name__)

# Task 1: Simulated data storage
inventory = [
    {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "ingredients_text": "Filtered water, almonds", "price": 4.99, "stock": 50},
    {"id": 2, "product_name": "Greek Yogurt", "brands": "Chobani", "ingredients_text": "Milk, cultures", "price": 1.50, "stock": 100}
]

def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.json
    if not data or 'product_name' not in data:
        abort(400, description="Missing product name")
    
    new_item = {
        "id": inventory[-1]['id'] + 1 if inventory else 1,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", "Generic"),
        "ingredients_text": data.get("ingredients_text", "N/A"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    item['price'] = data.get('price', item['price'])
    item['stock'] = data.get('stock', item['stock'])
    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [i for i in inventory if i['id'] != item_id]
    return jsonify({"result": True}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
