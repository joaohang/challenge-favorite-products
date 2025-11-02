from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.services.auth import AuthService
from app.domain.schemas.auth import TokenRequest, TokenResponse
from app.core.dependencies.auth import get_auth_service

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenResponse)
def get_access_token(
    request: TokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    if not auth_service.verify_api_token(request.token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )

    access_token, expires_in = auth_service.create_access_token()

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )


@router.delete("/revoke")
def revoke_token(
    token: str,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    revoked = auth_service.revoke_token(token)

    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found or already expired",
        )

    return {"message": "Token revoked successfully"}
