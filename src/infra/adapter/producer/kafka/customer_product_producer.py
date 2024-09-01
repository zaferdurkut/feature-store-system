import json

from opentracing_instrumentation import get_current_span
from pydantic import BaseModel

from src.infra.adapter.producer.kafka.producer_config import initialize_customer_product_producer
from src.infra.config.app_config import KAFKA_CUSTOMER_PRODUCT_TOPIC
from src.infra.config.logging_config import get_logger
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.infra_exception import InfraException

logger = get_logger()


class EventProducer:
    def __init__(self):
        self.kafka_event_producer = initialize_customer_product_producer()
        self.notification_topic = KAFKA_CUSTOMER_PRODUCT_TOPIC

    def create_event(
        self, customer_product_event_input_model: BaseModel
    ):
        with tracer.start_active_span(
            "EventProducer-create_customer_product_event",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "customer_product_event_input_model",
                customer_product_event_input_model,
            )
            self._send(
                topic=self.notification_topic,
                item=json.loads(customer_product_event_input_model.json()),
            )

    def _send(self, topic: str, item: dict):
        """Connect to Kafka and  push message to Topic"""
        self.kafka_event_producer.send(topic=topic, value=item).add_callback(
            EventProducer.on_send_success
        ).add_errback(EventProducer.on_send_error)

    @staticmethod
    def on_send_success(record):
        logger.info(f"Topic: {str(record.topic)}, Partition: {record.partition}")

    @staticmethod
    def on_send_error(exc):
        logger.error(str(exc))
        raise InfraException(error_code=2002, error_detail=exc)
