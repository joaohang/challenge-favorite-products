from rq import Queue
from app.infrastructure.cache.redis import get_redis_rq


def get_queue(name: str = "default") -> Queue:
    redis_conn = get_redis_rq()
    return Queue(name, connection=redis_conn)
