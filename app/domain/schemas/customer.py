from pydantic import BaseModel, EmailStr, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr


class Customer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
