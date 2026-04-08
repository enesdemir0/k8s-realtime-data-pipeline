import pytest
import requests_mock
from src.main import fetch_price, API_URL, SYMBOL

# 1. UNIT TEST (Matches CoinGecko format)
def test_fetch_price_mock():
    with requests_mock.Mocker() as m:
        # CoinGecko format
        m.get(API_URL, json={SYMBOL: {'usd': 50000.00}})
        price = fetch_price()
        assert price == '50000.00'

# 2. INTEGRATION TEST
def test_fetch_price_real_network():
    # Because the internet is flaky, we try up to 3 times
    price = None
    for _ in range(3):
        price = fetch_price()
        if price is not None:
            break
        time.sleep(2)
        
    assert price is not None
    assert isinstance(price, str)
    assert float(price) > 0