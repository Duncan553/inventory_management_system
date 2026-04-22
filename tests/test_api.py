import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_get_inventory(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert len(res.json) >= 2

def test_add_item(client):
    res = client.post('/inventory', json={"product_name": "Test", "price": 10.0})
    assert res.status_code == 201
