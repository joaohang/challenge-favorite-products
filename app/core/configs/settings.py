from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "Challenge Favorite Products"
    app_version: str = "0.1.0"
    log_level: str = "info"
    environment: str = "development"
    debug: bool = True if environment == "development" else False

    # API
    host: str = "0.0.0.0"
    port: int = 8000

    # DATABASE
    db_user: str = "challenge"
    db_pass: str = "I00OUjvpedxVeJq1"
    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "favorite_products"

    # REDIS
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
