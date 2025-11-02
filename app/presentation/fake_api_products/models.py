from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    id: str
    title: str
    price: float
    image: str
    brand: str
    reviewScore: Optional[float] = None


class ProductListResponse(BaseModel):
    items: List[Product]
    total: int
    page: int
    page_size: int
    total_pages: int
