# Inventory Management System (REST API)

A Flask-based REST API for managing retail inventory, integrated with the OpenFoodFacts API.

## Features
- **Full CRUD**: Create, Read, Update, and Delete inventory items.
- **External Integration**: Fetch product details using barcodes from OpenFoodFacts.
- **CLI Interface**: A user-friendly terminal tool to interact with the API.
- **Unit Testing**: Automated tests using `pytest`.

## Installation
1. Install dependencies:
   ```bash
   pip install flask requests pytest
Run the server:

Bash
python app.py
Run the CLI (in a separate terminal):

Bash
python cli.py
API Endpoints
GET /inventory - Fetch all items

POST /inventory - Add an item (Manual or Barcode)

PATCH /inventory/<id> - Update price/stock

DELETE /inventory/<id> - Remove an item

Testing
Run tests using:

Bash
pytest tests/test_api.py
