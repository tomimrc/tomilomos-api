"""SQLAlchemy declarative base for ORM models.

All database models should inherit from this Base class.
This module is imported by db/models.py and migration scripts.
"""

from sqlalchemy.orm import declarative_base

# Declarative base for all ORM models
Base = declarative_base()
