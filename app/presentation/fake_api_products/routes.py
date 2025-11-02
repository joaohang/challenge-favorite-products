from fastapi import APIRouter, HTTPException, Query
from .models import Product, ProductListResponse
from .database import FakeDatabase

router = APIRouter()
db = FakeDatabase()


@router.get("/api/product/", response_model=ProductListResponse)
async def list_products(page: int = Query(1, ge=1)):
    all_products = db.get_all_products()
    total = len(all_products)
    page_size = 5
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_products = all_products[start_idx:end_idx]

    return ProductListResponse(
        items=paginated_products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/api/product/{product_id}/", response_model=Product)
async def get_product_detail(product_id: str):
    product = db.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
