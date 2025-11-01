from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> Any:
    return {"status": "OK"}
