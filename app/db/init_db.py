from sqlalchemy import create_engine, text
from app.db.database import Base, engine
from app.cfg.config import settings
from pathlib import Path
from app.cfg.logging_config import get_logger

logger = get_logger(Path(__file__).stem)

# Create database if it doesn't exist
base_engine = create_engine(settings.database_url_base, isolation_level="AUTOCOMMIT")
with base_engine.connect() as conn:
    exists = conn.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
        {"db_name": settings.db_name},
    ).scalar()

    if not exists:
        conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
        logger.debug(f"Database {settings.db_name} created")
    else:
        logger.debug(f"Database {settings.db_name} already exists")

logger.debug(f"Tables to be created: {list(Base.metadata.tables.keys())}")
Base.metadata.create_all(bind=engine)
logger.debug("DB initialized")
