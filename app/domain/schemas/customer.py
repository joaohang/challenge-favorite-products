from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr


class CustomerRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
