import os
import time
import logging
import requests
import redis # New import

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SYMBOL = os.getenv("SYMBOL", "bitcoin")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={SYMBOL}&vs_currencies=usd"

# 1. Connect to Redis
# We use 'redis-service' because that's the name we gave it in the YAML!
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    logger.error(f"Could not connect to Redis: {e}")

def fetch_price():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = str(data[SYMBOL]['usd'])
        return price
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        return None

def main():
    logger.info(f"Starting Collector for {SYMBOL}...")
    while True:
        price = fetch_price()
        if price:
            # 2. Push price to Redis
            try:
                cache.set("latest_price", price)
                logger.info(f"Stored {SYMBOL} price {price} in Redis")
            except Exception as e:
                logger.error(f"Failed to push to Redis: {e}")
        
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()