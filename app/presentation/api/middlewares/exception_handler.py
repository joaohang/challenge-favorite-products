import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def _generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        f"""Unhandled exception:
        {request.method} {request.url.path} -
        {type(exc).__name__}: {str(exc)}
        """
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "type": type(exc).__name__,
            "path": request.url.path,
        },
    )


async def catch_exceptions_middleware(  # type: ignore[no-untyped-def]
    request: Request, call_next
):
    try:
        return await call_next(request)
    except Exception as exc:
        return await _generic_exception_handler(request, exc)
