import pytest
import requests_mock
import time
from src.main import fetch_price, API_URL, SYMBOL

# 1. UNIT TEST
def test_fetch_price_mock():
    with requests_mock.Mocker() as m:
        # CoinGecko format
        m.get(API_URL, json={SYMBOL: {'usd': 50000.00}})
        price = fetch_price()
        
        # FIX: Convert to float so '50000.0' equals '50000.00'
        assert float(price) == 50000.00

# 2. INTEGRATION TEST
def test_fetch_price_real_network():
    price = None
    for _ in range(3):
        price = fetch_price()
        if price is not None:
            break
        time.sleep(2)
        
    assert price is not None
    # We check that it's a valid number
    assert float(price) > 0