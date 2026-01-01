from tarantool import connect
from app.settings import settings
from app.logger import logger

_tarantool_connection = None


def get_tarantool_connection():
    global _tarantool_connection
    if _tarantool_connection is None:
        _tarantool_connection = connect(
            host=settings.TARANTOOL_HOST,
            port=settings.TARANTOOL_PORT,
            user=settings.TARANTOOL_USER,
            password=settings.TARANTOOL_PASSWORD,
        )
        logger.info(
            f"Connected to Tarantool at {settings.TARANTOOL_HOST}:{settings.TARANTOOL_PORT}"
        )
    return _tarantool_connection


def close_tarantool_connection():
    global _tarantool_connection
    if _tarantool_connection:
        _tarantool_connection.close()
        _tarantool_connection = None
        logger.info("Tarantool connection closed")
