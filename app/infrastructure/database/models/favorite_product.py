from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.infrastructure.database.postgres import Base


class FavoriteProduct(Base):
    __tablename__ = "favorite_products"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    product_id = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "customer_id", "product_id", name="uq_customer_product_favorite"
        ),
    )

    customer = relationship("Customer", back_populates="favorite_products")
