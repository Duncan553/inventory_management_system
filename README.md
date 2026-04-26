# Inventory Management System

A Flask-based REST API for managing retail inventory, with CLI interface and OpenFoodFacts integration.

## Features
- Full CRUD API (GET, POST, PATCH, DELETE)
- Helper routes: search, low-stock, barcode fetch
- CLI menu to interact with the API
- External API integration (OpenFoodFacts by barcode)
- 23 unit tests covering all features

## Setup
```bash
pip install -r requirements.txt
python3 app.py
```

## Run CLI
```bash
python3 cli.py
```

## Run Tests
```bash
python3 -m pytest tests/ -v
```

## API Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | /inventory | Get all items |
| GET | /inventory/<id> | Get one item |
| POST | /inventory | Add new item |
| PATCH | /inventory/<id> | Update item |
| DELETE | /inventory/<id> | Delete item |
| GET | /inventory/search?q= | Search by name |
| GET | /inventory/low-stock | Items with stock < 10 |
| POST | /inventory/fetch/<barcode> | Import from OpenFoodFacts |
