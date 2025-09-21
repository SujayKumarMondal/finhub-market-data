import os
import json
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

# Redis setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def cache_data(key: str, data: dict, expire: int = 3600):
    redis_client.setex(key, expire, json.dumps(data))

def get_cached_data(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

# Finnhub API key
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = os.environ.get("FINHUB_URL")

def fetch_finnhub_data(endpoint: str, params: dict):
    params["token"] = FINNHUB_API_KEY
    from requests import get
    response = get(f"{BASE_URL}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()
