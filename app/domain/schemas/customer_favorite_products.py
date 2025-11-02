from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class ProductDetail(BaseModel):
    id: str
    title: str
    price: float
    image: HttpUrl
    brand: str
    review_score: Optional[float] = Field(None, alias="reviewScore")


class FavoriteProductDetail(BaseModel):
    favorite_id: int
    product: ProductDetail
    review_url: Optional[HttpUrl] = None

    @classmethod
    def create(
        cls,
        favorite_id: int,
        product_data: dict,
        review_api_base_url: str,
    ) -> "FavoriteProductDetail":
        product = ProductDetail(**product_data)

        review_url: HttpUrl | None = None
        if product.review_score is not None:
            review_url = HttpUrl(
                url=f"{review_api_base_url}/product/{product.id}/"
            )

        return cls(
            favorite_id=favorite_id,
            product=product,
            review_url=review_url,
        )
