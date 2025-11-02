from fastapi import Depends
import redis

from app.domain.services.auth import AuthService
from app.infrastructure.cache.redis import get_redis


def get_auth_service(
    redis_client: redis.Redis = Depends(get_redis),
) -> AuthService:
    return AuthService(redis_client)
