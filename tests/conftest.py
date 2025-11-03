"""
Configurações e fixtures compartilhadas para os testes.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.configs.settings import Settings
from app.presentation.api.routes.auth import router
from app.infrastructure.cache.redis import get_redis
from tests.infrastructure.fake_redis import (
    override_get_redis,
    fake_redis_client,
)


class TestSettings(Settings):
    class Config:
        env_file = ".env.development"
        case_sensitive = False


@pytest.fixture(scope="session")
def test_settings():
    return TestSettings()


@pytest.fixture(scope="function")
def redis_client():
    fake_redis_client.__init__()
    return fake_redis_client


@pytest.fixture(scope="function")
def app(test_settings, redis_client):
    app = FastAPI()

    app.dependency_overrides[get_redis] = override_get_redis

    app.include_router(router)

    return app


@pytest.fixture(scope="function")
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def valid_jwt_token(client, test_settings):
    response = client.post(
        "/auth/token", json={"token": test_settings.api_token}
    )
    return response.json()["access_token"]
