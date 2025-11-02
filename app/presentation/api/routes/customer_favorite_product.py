from fastapi import APIRouter, Depends, Query, Path

from app.domain.services.customer_favorite_product import (
    CustomerFavoriteProductService,
)
from app.domain.schemas.customer_favorite_products import FavoriteProductDetail
from app.domain.schemas.pagination import PaginatedResponse
from app.core.dependencies.customer_favorite_product import (
    get_customer_favorite_product_service,
)

router = APIRouter()


@router.get(
    "/customers/{customer_id}/favorites-products",
    response_model=PaginatedResponse[FavoriteProductDetail],
)
def get_customer_favorites_with_products(
    customer_id: int = Path(..., description="Customer ID"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(
        default=10, ge=1, le=100, description="Items per page"
    ),
    service: CustomerFavoriteProductService = Depends(
        get_customer_favorite_product_service
    ),
) -> PaginatedResponse[FavoriteProductDetail]:
    skip = (page - 1) * page_size

    (
        favorites_with_details,
        total,
    ) = service.get_customer_favorites_with_details(
        customer_id=customer_id,
        skip=skip,
        limit=page_size,
    )

    return PaginatedResponse.create(
        items=favorites_with_details,
        total=total,
        page=page,
        page_size=page_size,
    )
