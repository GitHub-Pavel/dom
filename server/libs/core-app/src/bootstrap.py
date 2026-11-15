from os import getenv

from fastapi import FastAPI

from .logger import setup_logging


def bootstrap() -> FastAPI:
    setup_logging(getenv("SERVER_LOG_LEVEL", "INFO"))

    from .db.database import setup_sqlalchemy_logging

    setup_sqlalchemy_logging()

    app = FastAPI()
    return app
