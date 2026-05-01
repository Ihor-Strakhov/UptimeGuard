from sqlalchemy import create_engine, text
# from sqlalchemy.exc import ProgrammingError
from app.database import Base, engine
from app import models
from app.config import settings
from app.logging_config import get_logger

logger = get_logger(__name__)

# Create database if it doesn't exist
base_engine = create_engine(settings.database_url_base, isolation_level="AUTOCOMMIT")
with base_engine.connect() as conn:
    exists = conn.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
        {"db_name": settings.db_name},
    ).scalar()

    if not exists:
        conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
        logger.info(f"Database {settings.db_name} created")
    else:
        logger.info(f"Database {settings.db_name} already exists")

Base.metadata.create_all(bind=engine)
logger.info("DB initialized")