from fastapi import APIRouter, Depends, HTTPException, Path, status, Query

from app.domain.services.favorite_product import FavoriteProductService
from app.domain.schemas.favorite_product import (
    FavoriteProductCreate,
    FavoriteProduct,
)
from app.core.dependencies.favorite_product import get_favorite_product_service
from app.domain.schemas.pagination import PaginatedResponse

router = APIRouter()


@router.get(
    "/favorites/customers/{customer_id}",
    response_model=PaginatedResponse[FavoriteProduct],
)
def get_customer_favorites(
    customer_id: int = Path(..., ge=1, description="Customer ID"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(
        default=10, ge=1, le=100, description="Items per page"
    ),
    service: FavoriteProductService = Depends(get_favorite_product_service),
) -> PaginatedResponse[FavoriteProduct]:
    skip = (page - 1) * page_size
    favorites, total = service.get_customer_favorites(
        customer_id=customer_id,
        skip=skip,
        limit=page_size,
    )

    return PaginatedResponse.create(
        items=favorites,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/favorites/{favorite_id}",
    response_model=FavoriteProduct,
)
def get_favorite_by_id(
    favorite_id: int = Path(..., ge=1, description="Favorite ID"),
    service: FavoriteProductService = Depends(get_favorite_product_service),
) -> FavoriteProduct:
    try:
        return service.get_favorite_by_id(favorite_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/favorites",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
)
def add_to_favorites(
    favorite_data: FavoriteProductCreate,
    service: FavoriteProductService = Depends(get_favorite_product_service),
) -> dict:
    job_id = service.add_to_favorites_async(
        customer_id=favorite_data.customer_id,
        product_id=favorite_data.product_id,
    )
    return {
        "message": "Favorite creation enqueued successfully",
        "job_id": job_id,
        "status_url": f"/favorites/jobs/{job_id}",
    }


@router.delete(
    "/favorites",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
)
def remove_from_favorites(
    favorite_data: FavoriteProductCreate,
    service: FavoriteProductService = Depends(get_favorite_product_service),
) -> dict:
    job_id = service.remove_from_favorites_async(
        customer_id=favorite_data.customer_id,
        product_id=favorite_data.product_id,
    )
    return {
        "message": "Favorite deletion enqueued successfully",
        "job_id": job_id,
        "status_url": f"/favorites/jobs/{job_id}",
    }


@router.get(
    "/favorites/jobs/{job_id}",
    response_model=dict,
)
def get_job_status(
    job_id: str = Path(..., description="Job ID"),
    service: FavoriteProductService = Depends(get_favorite_product_service),
) -> dict:
    """Retorna o status de um job na fila"""
    try:
        return service.get_job_status(job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
