from typing import List, Tuple
from app.domain.schemas.customer import Customer, CustomerCreate
from app.domain.interfaces.customer import ICustomerRepository


class CustomerService:
    def __init__(self, repository: ICustomerRepository):
        self.repository = repository

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")
        return customer

    def get_customer_by_email(self, email: str) -> Customer:
        customer = self.repository.get_by_email(email)
        if not customer:
            raise ValueError(f"Customer with email {email} not found")
        return customer

    def get_all_customers(
        self, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Customer], int]:
        return self.repository.get_all(skip, limit)

    def create_customer(self, name: str, email: str) -> Customer:
        existing = self.repository.get_by_email(email)
        if existing:
            raise ValueError("Customer with this email already exists")

        customer_data = CustomerCreate(name=name, email=email)

        return self.repository.create(customer_data)

    def update_customer(
        self, customer_id: int, name: str, email: str
    ) -> Customer:
        existing_customer = self.repository.get_by_id(customer_id)
        if not existing_customer:
            raise ValueError(f"Customer with id {customer_id} not found")

        email_owner = self.repository.get_by_email(email)
        if email_owner and email_owner.id != customer_id:
            raise ValueError("Email already in use by another customer")

        customer_data = CustomerCreate(name=name, email=email)
        updated = self.repository.update(customer_id, customer_data)

        if not updated:
            raise ValueError(
                f"Failed to update customer with id {customer_id}"
            )

        return updated

    def delete_customer(self, customer_id: int) -> bool:
        existing = self.repository.get_by_id(customer_id)
        if not existing:
            raise ValueError(f"Customer with id {customer_id} not found")

        return self.repository.delete(customer_id)
