from sqlalchemy.orm import Session
from fastapi import Depends
import redis

from app.domain.services.customer_favorite_product import (
    CustomerFavoriteProductService,
)
from app.infrastructure.repositories.favorite_product import (
    FavoriteProductRepository,
)
from app.infrastructure.external.product_api import ProductAPI
from app.infrastructure.database.postgres import get_db
from app.infrastructure.cache.redis import get_redis


def get_customer_favorite_product_service(
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> CustomerFavoriteProductService:
    favorite_repository = FavoriteProductRepository(db, redis_client)
    product_api = ProductAPI(redis_client)
    return CustomerFavoriteProductService(favorite_repository, product_api)
