from sqlalchemy.orm import Session
from fastapi import Depends
import redis

from app.domain.services.favorite_product import FavoriteProductService
from app.infrastructure.repositories.favorite_product import (
    FavoriteProductRepository,
)
from app.infrastructure.database.postgres import get_db
from app.infrastructure.queue.rq_client import get_queue
from app.core.configs.settings import settings
from app.infrastructure.cache.redis import get_redis, get_redis_rq


def get_favorite_product_service(
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
    redis_rq: redis.Redis = Depends(get_redis_rq),
) -> FavoriteProductService:
    repository = FavoriteProductRepository(db, redis_client)
    queue = get_queue(settings.favorite_queue)
    return FavoriteProductService(repository, queue, redis_rq)
