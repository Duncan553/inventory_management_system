import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cli import run_cli
from utils import fetch_product_from_api

def test_fetch_product_success():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Orange Juice", "brands": "Tropicana", "ingredients_text": "Oranges"}
    }
    with patch('utils.requests.get', return_value=fake_response):
        result = fetch_product_from_api("123456")
    assert result['product_name'] == 'Orange Juice'

def test_fetch_product_not_found():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"status": 0}
    with patch('utils.requests.get', return_value=fake_response):
        result = fetch_product_from_api("000000")
    assert result is None

def test_fetch_product_api_error():
    with patch('utils.requests.get', side_effect=Exception("Network error")):
        result = fetch_product_from_api("999999")
    assert result is None

def test_cli_view_all(capsys):
    fake_response = MagicMock()
    fake_response.json.return_value = [{"id": 1, "product_name": "Milk"}]
    with patch('cli.requests.get', return_value=fake_response):
        with patch('builtins.input', side_effect=["1", "6"]):
            run_cli()
    captured = capsys.readouterr()
    assert "Milk" in captured.out

def test_cli_add_item():
    fake_response = MagicMock()
    fake_response.status_code = 201
    with patch('cli.requests.post', return_value=fake_response):
        with patch('builtins.input', side_effect=["2", "Test Milk", "3.50", "6"]):
            run_cli()

def test_cli_import_barcode_found(capsys):
    fake_product = {"product_name": "Barcode Juice", "brands": "BrandX", "ingredients_text": "Juice"}
    fake_post = MagicMock()
    with patch('cli.fetch_product_from_api', return_value=fake_product):
        with patch('cli.requests.post', return_value=fake_post):
            with patch('builtins.input', side_effect=["3", "1234567", "2.99", "10", "6"]):
                run_cli()
    captured = capsys.readouterr()
    assert "Found" in captured.out

def test_cli_import_barcode_not_found(capsys):
    with patch('cli.fetch_product_from_api', return_value=None):
        with patch('builtins.input', side_effect=["3", "0000000", "6"]):
            run_cli()
    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()

def test_cli_update_item():
    fake_response = MagicMock()
    with patch('cli.requests.patch', return_value=fake_response):
        with patch('builtins.input', side_effect=["4", "1", "9.99", "5", "6"]):
            run_cli()

def test_cli_delete_item():
    fake_response = MagicMock()
    with patch('cli.requests.delete', return_value=fake_response):
        with patch('builtins.input', side_effect=["5", "1", "6"]):
            run_cli()
