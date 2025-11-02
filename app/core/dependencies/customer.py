from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.interfaces.customer import ICustomerRepository
from app.domain.services.customer import CustomerService
from app.infrastructure.database.postgres import get_db
from app.infrastructure.cache.redis import get_redis
from app.infrastructure.repositories.customer import CustomerRepository

import redis


def get_customer_repository(
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> ICustomerRepository:
    return CustomerRepository(db, redis_client)


def get_customer_service(
    repository: ICustomerRepository = Depends(get_customer_repository),
) -> CustomerService:
    return CustomerService(repository)
