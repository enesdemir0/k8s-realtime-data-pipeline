import os
import time
import logging
import redis
import psycopg2 # New import

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Config
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "cryptodb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

def init_db():
    while True:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(10),
                    price FLOAT,
                    trend VARCHAR(10),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Postgres Database initialized.")
            break
        except Exception as e:
            logger.error(f"Waiting for Postgres... {e}")
            time.sleep(5)

def save_to_db(symbol, price, trend):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO prices (symbol, price, trend) VALUES (%s, %s, %s)",
            (symbol, price, trend)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Saved to Postgres: {symbol} at {price} ({trend})")
    except Exception as e:
        logger.error(f"Failed to save to Postgres: {e}")

def main():
    init_db()
    cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    last_price = None

    while True:
        current_price = cache.get("latest_price")
        if current_price:
            current_price = float(current_price)
            trend = "STABLE"
            if last_price is not None:
                if current_price > last_price: trend = "UP"
                elif current_price < last_price: trend = "DOWN"
            
            # SAVE TO DATABASE
            save_to_db("bitcoin", current_price, trend)
            last_price = current_price
            
        time.sleep(30)

if __name__ == "__main__":
    main()