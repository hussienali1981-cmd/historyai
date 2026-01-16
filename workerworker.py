import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from redis import Redis
from rq import Worker, Queue, Connection
from backend.app.config import REDIS_URL

redis_conn = Redis.from_url(REDIS_URL)
listen = ['default']

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
