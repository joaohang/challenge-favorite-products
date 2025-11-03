from fastapi import Depends
from fastapi.testclient import TestClient
from app.presentation.api.dependencies.auth import token_validator


class TestAuthToken:
    def test_get_access_token_success(
        self, client: TestClient, test_settings, redis_client
    ):
        valid_token = test_settings.api_token

        response = client.post("/v1/auth/token", json={"token": valid_token})

        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        cache_key = f"jwt:token:{data['access_token']}".encode("utf-8")
        assert redis_client.get(cache_key) == "valid"

    def test_get_access_token_invalid_token(self, client: TestClient):
        response = client.post(
            "/v1/auth/token",
            json={"token": "token-invalido-que-nao-esta-no-env"},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API token"}

    def test_get_access_token_missing_token(self, client: TestClient):
        response = client.post("/v1/auth/token", json={})

        assert response.status_code == 422

    def test_get_access_token_empty_token(self, client: TestClient):
        response = client.post("/v1/auth/token", json={"token": ""})

        assert response.status_code == 401


class TestAuthRevoke:
    def test_revoke_token_success(
        self,
        client: TestClient,
        test_settings,
        valid_jwt_token: str,
        redis_client,
    ):
        app = client.app

        @app.get("/v1/token-check", dependencies=[Depends(token_validator)])
        def token_check_route():
            return {"status": "validated"}

        valid_token = test_settings.api_token

        auth_response = client.post(
            "/v1/auth/token", json={"token": valid_token}
        )

        assert auth_response.status_code == 200

        revoke_response = client.delete(
            "/v1/auth/revoke", params={"token": valid_jwt_token}
        )

        assert revoke_response.status_code == 200
        assert revoke_response.json() == {
            "message": "Token revoked successfully"
        }

        customer_response = client.get("/v1/token-check")

        assert customer_response.status_code == 401
