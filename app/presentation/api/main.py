import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.configs.settings import settings

from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes.customer import router as customer_router
from app.presentation.api.routes.favorite_product import (
    router as favorite_product_router,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Api para cadastro de clientes e seus produtos favoritos",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(customer_router)
app.include_router(favorite_product_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level,
    )
