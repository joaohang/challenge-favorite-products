from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import redis

from app.domain.schemas.favorite_product import FavoriteProduct
from app.domain.interfaces.favorite_product import IFavoriteProductRepository
from app.infrastructure.database.models.favorite_product import (
    FavoriteProduct as FavoriteProductModel,
)
from app.infrastructure.external.product_api import ProductAPI


class FavoriteProductRepository(IFavoriteProductRepository):
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.product_api = ProductAPI(redis_client)

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

    def get_by_customer(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> Tuple[List[FavoriteProduct], int]:
        total = (
            self.db.query(FavoriteProductModel)
            .filter(FavoriteProductModel.customer_id == customer_id)
            .count()
        )

        db_favorites = (
            self.db.query(FavoriteProductModel)
            .filter(FavoriteProductModel.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        favorites = [
            FavoriteProduct.model_validate(fav)  # type: ignore[misc]
            for fav in db_favorites
        ]

        return favorites, total

    def create(self, customer_id: int, product_id: str) -> FavoriteProduct:
        product_data = self.product_api.get_product(product_id)
        if not product_data:
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
