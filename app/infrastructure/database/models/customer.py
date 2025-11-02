from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.postgres import Base


class Customer(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), nullable=False)
    email = Column(String(length=320), unique=True, nullable=False, index=True)

    favorite_products = relationship(
        "FavoriteProduct", back_populates="customer", lazy="selectin"
    )
