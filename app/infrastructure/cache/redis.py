import redis
from typing import Optional
from app.core.configs.settings import settings


class RedisClient:
    _instance: Optional[redis.Redis] = None
    _rq_instance: Optional[redis.Redis] = None

    @classmethod
    def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
        return cls._instance

    @classmethod
    def get_rq_instance(cls) -> redis.Redis:
        if cls._rq_instance is None:
            cls._rq_instance = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=False,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
        return cls._rq_instance

    @classmethod
    def close(cls) -> None:
        if cls._instance:
            cls._instance.close()
            cls._instance = None
        if cls._rq_instance:
            cls._rq_instance.close()
            cls._rq_instance = None


def get_redis() -> redis.Redis:
    return RedisClient.get_instance()


def get_redis_rq() -> redis.Redis:
    return RedisClient.get_rq_instance()
