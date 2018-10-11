"""Base model and base instance of db."""
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """Base class for all the tables.

    Consists of two default columns `created_at` and `modified_at` .
    """
    __abstract__ = True

    created_at = Column(DateTime,
                        default=datetime.datetime.utcnow)
    modified_at = Column(DateTime,
                         default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)
