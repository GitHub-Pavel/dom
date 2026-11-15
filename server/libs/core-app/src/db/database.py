import logging
import os
import sys
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from ..logger import InterceptHandler


def __getValue(key: str):
    value = os.getenv(key)
    if not value:
        logger.critical(f"The {key} environment variable is not set")
        sys.exit(1)
    return value


engine: AsyncEngine = create_async_engine(
    "postgresql+asyncpg://",
    echo=False,
    connect_args={
        "host": __getValue("PG_HOST"),
        "port": __getValue("PG_PORT"),
        "user": __getValue("PG_USER"),
        "password": __getValue("PG_PASSWORD"),
        "database": __getValue("PG_DATABASE"),
    },
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.exception(f"Error in the DB session: {e}")
            raise


def setup_sqlalchemy_logging() -> None:
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.handlers = [InterceptHandler()]
    sql_logger.setLevel(logging.INFO)
    sql_logger.propagate = False
