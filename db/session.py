"""SQLAlchemy database session and engine setup.

This module creates and manages the database engine and session factory.
The get_db() function is used as a FastAPI dependency to provide DB sessions to route handlers.
"""

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings


# Create engine with PostgreSQL connection string from config
# Use conditional pool settings based on database type
engine_kwargs = {
    "pool_pre_ping": True,  # Verify connections before using
}

# Only add pool settings for PostgreSQL (not for SQLite in testing)
if "postgresql" in settings.database_url:
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
    })

engine = create_engine(
    settings.database_url,
    **engine_kwargs
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """Get a database session for dependency injection.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
