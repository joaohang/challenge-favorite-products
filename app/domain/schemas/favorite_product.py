from pydantic import BaseModel


class FavoriteProductCreate(BaseModel):
    customer_id: int
    product_id: str


class FavoriteProductRead(BaseModel):
    id: int
    customer_id: int
    product_id: str

    class Config:
        orm_mode = True
