import os

import redis
from dotenv import load_dotenv


load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)


def test_redis():

    response = redis_client.ping()

    if response:
        print("[REDIS] Connected successfully!")
