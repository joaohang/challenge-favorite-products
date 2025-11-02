from pydantic import BaseModel, ConfigDict


class FavoriteProductCreate(BaseModel):
    customer_id: int
    product_id: str


class FavoriteProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    product_id: str
