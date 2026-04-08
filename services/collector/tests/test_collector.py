import pytest
import requests_mock
from src.main import fetch_price, API_URL

# 1. UNIT TEST (Fast & Safe)
def test_fetch_price_mock():
    with requests_mock.Mocker() as m:
        m.get(API_URL, json={'price': '50000.00'})
        price = fetch_price()
        assert price == '50000.00'

# 2. INTEGRATION TEST (Real Network)
# This actually calls Binance during the test!
def test_fetch_price_real_network():
    price = fetch_price()
    
    # We don't know the exact price of Bitcoin, 
    # but we know it should be a string and not None.
    assert price is not None
    assert isinstance(price, str)
    assert float(price) > 0