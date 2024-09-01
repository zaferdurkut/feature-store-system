import json

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from src.infra.config.app_config import (
    KAFKA_CUSTOMER_PRODUCT_SERVERS,
)
from src.infra.config.logging_config import get_logger
from src.infra.exception.infra_exception import InfraException

logger = get_logger()

def initialize_customer_product_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=KAFKA_CUSTOMER_PRODUCT_SERVERS,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
    except NoBrokersAvailable as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2000)
    except Exception as exc:
        logger.critical(str(exc))
        raise InfraException(error_code=2001)
