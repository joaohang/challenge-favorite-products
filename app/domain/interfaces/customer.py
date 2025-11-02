from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.schemas.customer import Customer, CustomerCreate


class ICustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_all(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Customer], int]:
        pass

    @abstractmethod
    def create(self, customer: CustomerCreate) -> Customer:
        pass

    @abstractmethod
    def update(
        self, customer_id: int, customer: CustomerCreate
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        pass
