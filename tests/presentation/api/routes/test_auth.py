from fastapi.testclient import TestClient


class TestAuthToken:
    def test_get_access_token_success(
        self, client: TestClient, test_settings, redis_client
    ):
        valid_token = test_settings.api_token

        response = client.post("/auth/token", json={"token": valid_token})

        assert response.status_code == 200

        data = response.json()
        expected_expiry = test_settings.jwt_access_token_expire_minutes * 60
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == expected_expiry

        cache_key = f"jwt:token:{data['access_token']}".encode("utf-8")
        assert redis_client.get(cache_key) == b"valid"

    def test_get_access_token_invalid_token(self, client: TestClient):
        """Testa a geração de token com API token inválido."""
        response = client.post(
            "/auth/token", json={"token": "token-invalido-que-nao-esta-no-env"}
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API token"}

    def test_get_access_token_missing_token(self, client: TestClient):
        """Testa a geração de token sem enviar o token."""
        response = client.post("/auth/token", json={})

        assert response.status_code == 422

    def test_get_access_token_empty_token(self, client: TestClient):
        """Testa a geração de token com token vazio."""
        response = client.post("/auth/token", json={"token": ""})

        assert response.status_code == 401


class TestAuthRevoke:
    def test_revoke_token_success(
        self, client: TestClient, valid_jwt_token: str, redis_client
    ):
        cache_key = f"jwt:token:{valid_jwt_token}".encode("utf-8")

        assert redis_client.get(cache_key) is not None

        response = client.delete(
            "/auth/revoke", params={"token": valid_jwt_token}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Token revoked successfully"}

        assert redis_client.get(cache_key) is None

    def test_revoke_token_nonexistent(self, client: TestClient):
        fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.token"

        response = client.delete("/auth/revoke", params={"token": fake_token})

        assert response.status_code == 200

    def test_revoke_token_missing_parameter(self, client: TestClient):
        response = client.delete("/auth/revoke")

        assert response.status_code == 422

    def test_revoke_token_twice(
        self, client: TestClient, valid_jwt_token: str
    ):
        response1 = client.delete(
            "/auth/revoke", params={"token": valid_jwt_token}
        )
        assert response1.status_code == 200

        response2 = client.delete(
            "/auth/revoke", params={"token": valid_jwt_token}
        )
        assert response2.status_code == 200
