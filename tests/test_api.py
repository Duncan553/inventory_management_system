import pytest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app as app_module
from app import app

@pytest.fixture(autouse=True)
def reset_inventory():
    app_module.inventory = [
        {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "ingredients_text": "Filtered water, almonds", "price": 4.99, "stock": 50},
        {"id": 2, "product_name": "Greek Yogurt", "brands": "Chobani", "ingredients_text": "Milk, cultures", "price": 1.50, "stock": 100}
    ]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_get_all_inventory(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert len(res.json) == 2

def test_get_single_item(client):
    res = client.get('/inventory/1')
    assert res.status_code == 200
    assert res.json['product_name'] == 'Organic Almond Milk'

def test_get_item_not_found(client):
    res = client.get('/inventory/999')
    assert res.status_code == 404

def test_add_item(client):
    res = client.post('/inventory', json={"product_name": "Test Juice", "price": 2.50, "stock": 30})
    assert res.status_code == 201
    assert res.json['product_name'] == 'Test Juice'

def test_add_item_missing_name(client):
    res = client.post('/inventory', json={"price": 5.0})
    assert res.status_code == 400

def test_update_item(client):
    res = client.patch('/inventory/1', json={"price": 9.99, "stock": 20})
    assert res.status_code == 200
    assert res.json['price'] == 9.99

def test_update_item_not_found(client):
    res = client.patch('/inventory/999', json={"price": 1.0})
    assert res.status_code == 404

def test_delete_item(client):
    res = client.delete('/inventory/1')
    assert res.status_code == 200
    assert res.json['result'] == True
    check = client.get('/inventory/1')
    assert check.status_code == 404

def test_delete_item_not_found(client):
    res = client.delete('/inventory/999')
    assert res.status_code == 404

def test_search_inventory(client):
    res = client.get('/inventory/search?q=yogurt')
    assert res.status_code == 200
    assert len(res.json) == 1

def test_search_no_results(client):
    res = client.get('/inventory/search?q=xyz999')
    assert res.status_code == 200
    assert res.json == []

def test_low_stock_route(client):
    client.post('/inventory', json={"product_name": "Low Item", "price": 1.0, "stock": 3})
    res = client.get('/inventory/low-stock')
    assert res.status_code == 200
    names = [i['product_name'] for i in res.json]
    assert 'Low Item' in names

def test_fetch_and_add_success(client):
    fake_product = {"product_name": "Fake Juice", "brands": "FakeCo", "ingredients_text": "Water"}
    with patch('app.fetch_product_from_api', return_value=fake_product):
        res = client.post('/inventory/fetch/1234567890', json={"price": 3.50, "stock": 20})
    assert res.status_code == 201
    assert res.json['product_name'] == 'Fake Juice'

def test_fetch_and_add_not_found(client):
    with patch('app.fetch_product_from_api', return_value=None):
        res = client.post('/inventory/fetch/0000000000')
    assert res.status_code == 404
