import redis

from src.infra.config.app_config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USER_DB,
    BATCH_REDIS_PORT,
    BATCH_REDIS_USER_DB,
    BATCH_REDIS_HOST,
)
from src.infra.exception.connection_exception import ConnectionException


def get_stream_redis_client():
    try:  #
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_USER_DB)
        redis_client.ping()
    except Exception as _:
        raise ConnectionException(error_code=1400)
    return redis_client


def get_offline_redis_client():
    try:  #
        redis_client = redis.Redis(
            host=BATCH_REDIS_HOST, port=BATCH_REDIS_PORT, db=BATCH_REDIS_USER_DB
        )
        redis_client.ping()
    except Exception as _:
        raise ConnectionException(error_code=1400)

    return redis_client
