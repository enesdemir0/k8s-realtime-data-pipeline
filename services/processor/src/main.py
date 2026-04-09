import os
import time
import logging
import redis

# 1. Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
PROCESS_INTERVAL = int(os.getenv("PROCESS_INTERVAL", 30))

def main():
    logger.info("Starting Processor Service...")
    
    # Connect to Redis
    try:
        cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        return

    last_price = None

    while True:
        try:
            # 3. Pull data from Redis
            current_price = cache.get("latest_price")
            
            if current_price:
                current_price = float(current_price)
                
                if last_price is not None:
                    # 4. Calculate the difference
                    diff = current_price - last_price
                    if diff > 0:
                        logger.info(f"TREND: 📈 UP | Price: {current_price} | Change: +{diff:.2f}")
                    elif diff < 0:
                        logger.info(f"TREND: 📉 DOWN | Price: {current_price} | Change: {diff:.2f}")
                    else:
                        logger.info(f"TREND: ➖ STABLE | Price: {current_price}")
                else:
                    logger.info(f"First price received: {current_price}")
                
                last_price = current_price
            else:
                logger.warning("No data found in Redis yet. Waiting...")

        except Exception as e:
            logger.error(f"Error in processing: {e}")

        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    main()