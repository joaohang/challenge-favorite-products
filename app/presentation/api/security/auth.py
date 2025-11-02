from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis

from app.domain.services.auth import AuthService
from app.infrastructure.cache.redis import get_redis

security_scheme = HTTPBearer(
    scheme_name="Bearer",
    description="JWT token de autenticação. Use o formato: Bearer <token>",
    auto_error=False,
)


async def token_validator(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    redis_client: redis.Redis = Depends(get_redis),
) -> str:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    auth_service = AuthService(redis_client)

    if not auth_service.verify_access_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
