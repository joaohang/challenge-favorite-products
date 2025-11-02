from fastapi import APIRouter, Depends, HTTPException, Query, Path

from app.domain.services.customer import CustomerService
from app.domain.schemas.customer import CustomerCreate, Customer
from app.domain.schemas.pagination import PaginatedResponse
from app.core.dependencies.customer import get_customer_service

router = APIRouter()


@router.get("/customers", response_model=PaginatedResponse[Customer])
def get_all_customers(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(
        default=10, ge=1, le=100, description="Items per page"
    ),
    service: CustomerService = Depends(get_customer_service),
) -> PaginatedResponse[Customer]:
    skip = (page - 1) * page_size
    customers, total = service.get_all_customers(skip=skip, limit=page_size)

    return PaginatedResponse.create(
        items=customers, total=total, page=page, page_size=page_size
    )


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer_by_id(
    customer_id: int = Path(..., ge=1, description="Customer ID"),
    service: CustomerService = Depends(get_customer_service),
) -> Customer:
    try:
        return service.get_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/customers/email/{email}", response_model=Customer)
def get_customer_by_email(
    email: str = Path(..., description="Customer email"),
    service: CustomerService = Depends(get_customer_service),
) -> Customer:
    try:
        return service.get_customer_by_email(email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/customers", response_model=Customer, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
) -> Customer:
    try:
        return service.create_customer(
            name=customer_data.name, email=customer_data.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(
    customer_data: CustomerCreate,
    customer_id: int = Path(..., ge=1, description="Customer ID"),
    service: CustomerService = Depends(get_customer_service),
) -> Customer:
    try:
        return service.update_customer(
            customer_id=customer_id,
            name=customer_data.name,
            email=customer_data.email,
        )
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))


@router.delete("/customers/{customer_id}", status_code=204)
def delete_customer(
    customer_id: int = Path(..., ge=1, description="Customer ID"),
    service: CustomerService = Depends(get_customer_service),
) -> None:
    try:
        service.delete_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
