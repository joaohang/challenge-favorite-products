from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.schemas.favorite_product import FavoriteProduct


class IFavoriteProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, favorite_id: int) -> Optional[FavoriteProduct]:
        pass

    @abstractmethod
    def get_by_customer(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> Tuple[List[FavoriteProduct], int]:
        pass

    @abstractmethod
    def create(self, customer_id: int, product_id: str) -> FavoriteProduct:
        pass

    @abstractmethod
    def delete_by_customer_and_product(
        self, customer_id: int, product_id: str
    ) -> bool:
        pass
