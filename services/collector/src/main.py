import os
import time
import logging
import requests

# 1. Setup Logging (This is how professionals monitor their apps)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Configuration (We get these from Environment Variables)
# If the variable isn't found, we use a default value (BTCUSDT)
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
API_URL = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"

def fetch_price():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status() # Check if the request was successful
        data = response.json()
        price = data['price']
        logger.info(f"Successfully fetched {SYMBOL} price: {price}")
        return price
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        return None

def main():
    logger.info(f"Starting Collector for {SYMBOL}...")
    while True:
        price = fetch_price()
        
        # Later, we will add the code to send this price to Service B (Redis)
        # For now, we just "collect" it.
        
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()