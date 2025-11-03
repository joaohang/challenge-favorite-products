from fastapi import Depends
import redis

from app.domain.services.auth import AuthService
from app.infrastructure.cache.redis import get_redis
from app.core.configs.settings import Settings
from .settings import get_settings


def get_auth_service(
    redis_client: redis.Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(redis_client, settings)
