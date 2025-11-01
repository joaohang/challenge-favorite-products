from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.configs.settings import settings

DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_pass}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

engine = create_engine(DATABASE_URL, future=True, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
