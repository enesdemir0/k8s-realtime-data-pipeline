import pytest
import requests_mock
from src.main import fetch_price, API_URL

# 1. UNIT TEST (Mocking the new CoinCap structure)
def test_fetch_price_mock():
    with requests_mock.Mocker() as m:
        # CoinCap returns a 'data' object
        m.get(API_URL, json={'data': {'priceUsd': '50000.00'}})
        price = fetch_price()
        assert price == '50000.00'

# 2. INTEGRATION TEST (Real Network to CoinCap)
def test_fetch_price_real_network():
    price = fetch_price()
    assert price is not None
    assert isinstance(price, str)
    assert float(price) > 0