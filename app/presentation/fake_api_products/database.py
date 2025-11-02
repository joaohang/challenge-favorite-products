from typing import List, Optional
from .models import Product


class FakeDatabase:
    def __init__(self):
        self.products = [
            Product(
                id="550e8400-e29b-41d4-a716-446655440000",
                title="Smartphone Galaxy Pro",
                price=1299.99,
                image="https://example.com/images/galaxy-pro.jpg",
                brand="Samsung",
                reviewScore=4.5,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440001",
                title="iPhone 15 Max",
                price=2499.99,
                image="https://example.com/images/iphone-15.jpg",
                brand="Apple",
                reviewScore=4.8,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440002",
                title="Notebook Inspiron 15",
                price=3499.99,
                image="https://example.com/images/inspiron.jpg",
                brand="Dell",
                reviewScore=4.2,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440003",
                title="Tablet Fire HD",
                price=299.99,
                image="https://example.com/images/fire-hd.jpg",
                brand="Amazon",
                reviewScore=4.0,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440004",
                title="Smartwatch Series 9",
                price=799.99,
                image="https://example.com/images/watch-series.jpg",
                brand="Apple",
                reviewScore=4.7,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440005",
                title="Headphones WH-1000XM5",
                price=899.99,
                image="https://example.com/images/wh1000xm5.jpg",
                brand="Sony",
                reviewScore=4.6,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440006",
                title="Mouse Gamer Pro",
                price=199.99,
                image="https://example.com/images/mouse-gamer.jpg",
                brand="Logitech",
                reviewScore=4.4,
            ),
            Product(
                id="550e8400-e29b-41d4-a716-446655440007",
                title="Monitor Ultra HD 4K",
                price=1899.99,
                image="https://example.com/images/monitor-4k.jpg",
                brand="LG",
                reviewScore=None,
            ),
        ]

    def get_all_products(self) -> List[Product]:
        return self.products

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        for product in self.products:
            if product.id == product_id:
                return product
        return None
