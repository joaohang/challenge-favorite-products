import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.core.configs.settings import Settings
from app.presentation.api.routes.auth import router as auth_router
from app.presentation.api.routes.customer import router as customer_router
from app.infrastructure.cache.redis import get_redis
from app.infrastructure.database.postgres import get_db
from tests.infrastructure.fake_redis import (
    override_get_redis,
    fake_redis_client,
)
from tests.infrastructure.fake_db import (
    override_get_db as override_fake_db,
    fake_db_instance,
)
from app.core.dependencies.settings import get_settings


class TestSettings(Settings):
    class Config:
        env_file = ".env.development"
        case_sensitive = False


@pytest.fixture(scope="function")
def test_settings():
    return TestSettings()


@pytest.fixture(scope="function")
def redis_client():
    fake_redis_client.clear()
    return fake_redis_client


@pytest.fixture(scope="function")
def db_session():
    fake_db_instance.clear()
    return fake_db_instance


@pytest.fixture(scope="function")
def app(test_settings, redis_client, db_session):
    app = FastAPI()

    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_db] = override_fake_db

    app.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
    app.include_router(
        customer_router,
        prefix="/v1",
        tags=["customers"],
    )

    return app


@pytest.fixture(scope="function")
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def valid_jwt_token(client, test_settings):
    response = client.post(
        "/v1/auth/token", json={"token": test_settings.api_token}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def sample_customer_data():
    return {"name": "John Doe", "email": "john.doe@example.com"}


@pytest.fixture(scope="function")
def created_customer(client, sample_customer_data):
    response = client.post("/v1/customers", json=sample_customer_data)
    assert (
        response.status_code == 201
    ), f"Failed to create customer: {response.json()}"
    return response.json()


@pytest.fixture(scope="function")
def multiple_customers(client):
    customers = []
    for i in range(5):
        customer_data = {
            "name": f"Customer {i}",
            "email": f"customer{i}@example.com",
        }
        response = client.post("/v1/customers", json=customer_data)
        assert response.status_code == 201
        customers.append(response.json())

    return customers
