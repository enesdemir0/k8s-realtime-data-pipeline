import os
import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CoinCap uses IDs like 'bitcoin' or 'ethereum'
SYMBOL = os.getenv("SYMBOL", "bitcoin")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
# New API URL
API_URL = f"https://api.coincap.io/v2/assets/{SYMBOL}"

def fetch_price():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        # CoinCap structure is data -> priceUsd
        price = data['data']['priceUsd']
        logger.info(f"Successfully fetched {SYMBOL} price: {price}")
        return price
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        return None

def main():
    logger.info(f"Starting Collector for {SYMBOL}...")
    while True:
        fetch_price()
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()