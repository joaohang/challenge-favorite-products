from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import redis

from app.domain.schemas.favorite_product import FavoriteProduct
from app.domain.interfaces.favorite_product import IFavoriteProductRepository
from app.infrastructure.database.models.favorite_product import (
    FavoriteProduct as FavoriteProductModel,
)
from app.infrastructure.external.product_api import ProductAPIClient


class FavoriteProductRepository(IFavoriteProductRepository):
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.product_api = ProductAPIClient(redis_client)

    def get_by_id(self, favorite_id: int) -> Optional[FavoriteProduct]:
        db_favorite = (
            self.db.query(FavoriteProductModel)
            .filter(FavoriteProductModel.id == favorite_id)
            .first()
        )
        if db_favorite:
            return FavoriteProduct.model_validate(
                db_favorite
            )  # type: ignore[no-any-return]
        return None

    def get_by_customer(self, customer_id: int) -> List[FavoriteProduct]:
        db_favorites = (
            self.db.query(FavoriteProductModel)
            .filter(FavoriteProductModel.customer_id == customer_id)
            .all()
        )
        return [
            FavoriteProduct.model_validate(fav)  # type: ignore[misc]
            for fav in db_favorites
        ]

    def create(self, customer_id: int, product_id: str) -> FavoriteProduct:
        if not self.product_api.product_exists(product_id):
            raise ValueError(f"Product {product_id} does not exist")

        db_favorite = FavoriteProductModel(
            customer_id=customer_id, product_id=product_id
        )
        try:
            self.db.add(db_favorite)
            self.db.commit()
            self.db.refresh(db_favorite)
            return FavoriteProduct.model_validate(
                db_favorite
            )  # type: ignore[no-any-return]
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Product already in favorites")

    def delete_by_customer_and_product(
        self, customer_id: int, product_id: str
    ) -> bool:
        db_favorite = (
            self.db.query(FavoriteProductModel)
            .filter(
                FavoriteProductModel.customer_id == customer_id,
                FavoriteProductModel.product_id == product_id,
            )
            .first()
        )
        if db_favorite:
            self.db.delete(db_favorite)
            self.db.commit()
            return True
        return False
