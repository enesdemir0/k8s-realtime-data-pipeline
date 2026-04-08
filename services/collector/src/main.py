import os
import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CoinGecko uses IDs like 'bitcoin'
SYMBOL = os.getenv("SYMBOL", "bitcoin")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
# New robust URL
API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={SYMBOL}&vs_currencies=usd"

def fetch_price():
    try:
        # We try to call the API
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # CoinGecko returns: {"bitcoin": {"usd": 65000.00}}
        price = str(data[SYMBOL]['usd'])
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