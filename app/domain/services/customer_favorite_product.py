from typing import List, Tuple
from app.domain.schemas.customer_favorite_products import FavoriteProductDetail
from app.domain.interfaces.favorite_product import IFavoriteProductRepository
from app.domain.interfaces.product_api import IProductAPI
from app.core.configs.settings import settings


class CustomerFavoriteProductService:
    def __init__(
        self,
        favorite_repository: IFavoriteProductRepository,
        product_api_client: IProductAPI,
    ):
        self.favorite_repository = favorite_repository
        self.product_api_client = product_api_client
        self.review_api_base_url = settings.review_api_url

    def get_customer_favorites_with_details(
        self, customer_id: int, skip: int = 0, limit: int = 10
    ) -> Tuple[List[FavoriteProductDetail], int]:
        favorites, total = self.favorite_repository.get_by_customer(
            customer_id, skip, limit
        )

        if not favorites:
            return [], total

        product_ids = [fav.product_id for fav in favorites]

        products_data = self.product_api_client.get_products_batch(product_ids)

        favorites_with_details: List[FavoriteProductDetail] = []

        for favorite in favorites:
            product_data = products_data.get(favorite.product_id)

            if not product_data:
                continue

            favorite_detail = FavoriteProductDetail.create(
                favorite_id=favorite.id,
                product_data=product_data,
                review_api_base_url=self.review_api_base_url,
            )

            favorites_with_details.append(favorite_detail)

        return favorites_with_details, total
