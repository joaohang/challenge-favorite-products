import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.configs.settings import settings

from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes.customer import router as customer_router
from app.presentation.api.routes.favorite_product import (
    router as favorite_product_router,
)
from app.presentation.api.routes.customer_favorite_product import (
    router as customer_favorite_product_router,
)
from app.presentation.api.middlewares.exception_handler import (
    catch_exceptions_middleware,
)
from app.presentation.api.security.auth import token_validator
from app.presentation.api.routes.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Api para cadastro de clientes e seus produtos favoritos",
    debug=settings.debug,
)

app.middleware("http")(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router, tags=["Service Health"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(
    customer_router,
    prefix="/v1",
    tags=["Customer Routes"],
    dependencies=[Depends(token_validator)],
)
app.include_router(
    favorite_product_router,
    prefix="/v1",
    tags=["Favorite Product Routes"],
    dependencies=[Depends(token_validator)],
)
app.include_router(
    customer_favorite_product_router,
    prefix="/v1/bff",
    tags=["BFF Routes"],
    dependencies=[Depends(token_validator)],
)

if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level,
    )
