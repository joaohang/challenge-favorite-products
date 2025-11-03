from datetime import datetime, timedelta
from jose import jwt, JWTError
import redis

from app.core.configs.settings import Settings


class AuthService:
    def __init__(self, redis_client: redis.Redis, settings: Settings):
        self.redis = redis_client
        self.api_token = settings.api_token
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = (
            settings.jwt_access_token_expire_minutes
        )

    def _get_token_cache_key(self, token: str) -> str:
        return f"jwt:token:{token}"

    def verify_api_token(self, token: str) -> bool:
        return token == self.api_token

    def create_access_token(self) -> tuple[str, int]:
        expire = datetime.utcnow() + timedelta(
            minutes=self.access_token_expire_minutes
        )
        expires_in = self.access_token_expire_minutes * 60

        to_encode = {
            "sub": "microservice",
            "exp": expire,
        }

        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )

        cache_key = self._get_token_cache_key(encoded_jwt)
        self.redis.setex(cache_key, expires_in, "valid")

        return encoded_jwt, expires_in

    def verify_access_token(self, token: str) -> bool:
        cache_key = self._get_token_cache_key(token)
        cached = self.redis.get(cache_key)

        if not cached:
            return False

        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True
        except JWTError:
            return False

    def revoke_token(self, token: str) -> bool:
        cache_key = self._get_token_cache_key(token)
        self.redis.delete(cache_key)
        return True
