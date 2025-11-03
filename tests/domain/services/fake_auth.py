from typing import Tuple


class FakeAuthService:
    VALID_API_TOKEN = "valid-api-token"
    MOCKED_ACCESS_TOKEN = "mocked_access_token_from_fake"
    REVOCABLE_TOKEN = "existing-token"
    EXPIRES_IN = 3600

    def verify_api_token(self, token: str) -> bool:
        return token == self.VALID_API_TOKEN

    def create_access_token(self) -> Tuple[str, int]:
        return (self.MOCKED_ACCESS_TOKEN, self.EXPIRES_IN)

    def revoke_token(self, token: str) -> bool:
        return token == self.REVOCABLE_TOKEN


mock_service = FakeAuthService()


def override_get_auth_service():
    return mock_service
