from fastapi.testclient import TestClient
from app.presentation.api.main import app


def test_health_enpoint():
    client = TestClient(app)

    response = client.get("/health")

    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "OK"
