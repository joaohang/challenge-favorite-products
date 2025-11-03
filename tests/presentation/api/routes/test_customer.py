from fastapi.testclient import TestClient


class TestGetAllCustomers:
    def test_get_all_customers_with_data(self, client: TestClient):
        customer1 = {"name": "Alice", "email": "alice@example.com"}
        customer2 = {"name": "Bob", "email": "bob@example.com"}

        client.post("/v1/customers", json=customer1)
        client.post("/v1/customers", json=customer2)

        response = client.get("/v1/customers")

        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 2
        assert data["total"] == 2
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["total_pages"] == 1

    def test_get_all_customers_pagination(self, client: TestClient):
        for i in range(15):
            client.post(
                "/v1/customers",
                json={"name": f"User {i}", "email": f"user{i}@example.com"},
            )

        response = client.get("/v1/customers?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["total_pages"] == 2

        response = client.get("/v1/customers?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 5
        assert data["total"] == 15
        assert data["page"] == 2


class TestGetCustomerById:
    def test_get_customer_by_id_success(
        self, client: TestClient, created_customer
    ):
        customer_id = created_customer["id"]

        response = client.get(f"/v1/customers/{customer_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == customer_id
        assert data["name"] == created_customer["name"]
        assert data["email"] == created_customer["email"]

    def test_get_customer_by_id_not_found(self, client: TestClient):
        response = client.get("/v1/customers/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestGetCustomerByEmail:
    def test_get_customer_by_email_success(
        self, client: TestClient, created_customer
    ):
        email = created_customer["email"]

        response = client.get(f"/v1/customers/email/{email}")

        assert response.status_code == 200
        data = response.json()

        assert data["email"] == email
        assert data["name"] == created_customer["name"]

    def test_get_customer_by_email_not_found(self, client: TestClient):
        response = client.get("/v1/customers/email/nonexistent@example.com")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateCustomer:
    def test_create_customer_success(
        self, client: TestClient, sample_customer_data
    ):
        response = client.post("/v1/customers", json=sample_customer_data)

        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["name"] == sample_customer_data["name"]
        assert data["email"] == sample_customer_data["email"]

    def test_create_customer_duplicate_email(
        self, client: TestClient, created_customer
    ):
        duplicate_data = {
            "name": "Different Name",
            "email": created_customer["email"],
        }

        response = client.post("/v1/customers", json=duplicate_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Customer with this email already exists"
        }

    def test_create_customer_invalid_email(self, client: TestClient):
        invalid_data = {"name": "John Doe", "email": "invalid-email"}

        response = client.post("/v1/customers", json=invalid_data)
        assert response.status_code == 422

    def test_create_customer_missing_name(self, client: TestClient):
        invalid_data = {"email": "john@example.com"}

        response = client.post("/v1/customers", json=invalid_data)
        assert response.status_code == 422

    def test_create_customer_missing_email(self, client: TestClient):
        invalid_data = {"name": "John Doe"}

        response = client.post("/v1/customers", json=invalid_data)
        assert response.status_code == 422


class TestUpdateCustomer:
    def test_update_customer_success(
        self, client: TestClient, created_customer
    ):
        customer_id = created_customer["id"]
        update_data = {"name": "Updated Name", "email": "updated@example.com"}

        response = client.put(f"/v1/customers/{customer_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == customer_id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]

    def test_update_customer_not_found(self, client: TestClient):
        update_data = {"name": "Updated Name", "email": "updated@example.com"}

        response = client.put("/v1/customers/999", json=update_data)

        assert response.status_code == 404
        assert response.json() == {"detail": "Customer with id 999 not found"}

    def test_update_customer_duplicate_email(self, client: TestClient):
        customer1 = client.post(
            "/v1/customers",
            json={"name": "Customer 1", "email": "customer1@example.com"},
        ).json()

        customer2 = client.post(
            "/v1/customers",
            json={"name": "Customer 2", "email": "customer2@example.com"},
        ).json()

        update_data = {"name": "Updated Name", "email": customer1["email"]}

        response = client.put(
            f"/v1/customers/{customer2['id']}", json=update_data
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Email already in use by another customer"
        }


class TestDeleteCustomer:
    def test_delete_customer_success(
        self, client: TestClient, created_customer
    ):
        customer_id = created_customer["id"]

        response = client.delete(f"/v1/customers/{customer_id}")

        assert response.status_code == 204

        get_response = client.get(f"/v1/customers/{customer_id}")
        assert get_response.status_code == 404
