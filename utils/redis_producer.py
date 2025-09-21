# utils/redis_producer.py
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def publish_message(stream_name: str, message: dict):
    """Publish a message to a Redis stream."""
    message_json = json.dumps(message)
    redis_client.xadd(stream_name, {"data": message_json})
    print(f"Published to {stream_name}: {message}")
