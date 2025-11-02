from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
import redis

from app.domain.schemas.customer import Customer, CustomerCreate
from app.domain.interfaces.customer import ICustomerRepository
from app.infrastructure.database.models.customer import (
    Customer as CustomerModel,
)
from app.core.configs.settings import settings


class CustomerRepository(ICustomerRepository):
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client
        self.cache_ttl = settings.cache_ttl_seconds

    def _get_email_cache_key(self, email: str) -> str:
        return f"customer:email:{email.lower()}"

    def _cache_customer_email(self, customer: Customer) -> None:
        key = self._get_email_cache_key(customer.email)
        self.redis.setex(key, self.cache_ttl, str(customer.id))

    def _remove_customer_email_cache(self, email: str) -> None:
        key = self._get_email_cache_key(email)
        self.redis.delete(key)

    def _check_email_exists_in_cache(self, email: str) -> Optional[int]:
        key = self._get_email_cache_key(email)
        customer_id = self.redis.get(key)
        if customer_id:
            return int(str(customer_id))
        return None

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        db_customer = (
            self.db.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )
        if db_customer:
            return Customer.model_validate(db_customer)
        return None

    def get_by_email(self, email: str) -> Optional[Customer]:
        cached_id = self._check_email_exists_in_cache(email)
        if cached_id:
            return self.get_by_id(cached_id)

        db_customer = (
            self.db.query(CustomerModel)
            .filter(CustomerModel.email == email)
            .first()
        )
        if db_customer:
            customer = Customer.model_validate(db_customer)
            self._cache_customer_email(customer)
            return customer

        return None

    def get_all(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Customer], int]:
        total = self.db.query(CustomerModel).count()
        db_customers = (
            self.db.query(CustomerModel).offset(skip).limit(limit).all()
        )

        customers = [Customer.model_validate(c) for c in db_customers]

        return customers, total

    def create(self, customer: CustomerCreate) -> Customer:
        db_customer = CustomerModel(name=customer.name, email=customer.email)
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)

        new_customer = Customer.model_validate(db_customer)

        self._cache_customer_email(new_customer)

        return new_customer

    def update(
        self, customer_id: int, customer: CustomerCreate
    ) -> Optional[Customer]:
        db_customer = (
            self.db.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )
        if db_customer:
            old_email = str(db_customer.email)
            self._remove_customer_email_cache(old_email)

            db_customer.name = customer.name  # type: ignore[assignment]
            db_customer.email = customer.email  # type: ignore[assignment]

            self.db.commit()
            self.db.refresh(db_customer)

            updated_customer = Customer.model_validate(db_customer)

            self._cache_customer_email(updated_customer)

            return updated_customer
        return None

    def delete(self, customer_id: int) -> bool:
        db_customer = (
            self.db.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )
        if db_customer:
            email = str(db_customer.email)
            self._remove_customer_email_cache(email)

            self.db.delete(db_customer)
            self.db.commit()
            return True
        return False
