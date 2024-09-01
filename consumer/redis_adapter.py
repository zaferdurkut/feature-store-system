import json
import logging
import os
import time
from typing import Any

import redis
from dotenv import load_dotenv
from pyflink.common import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer

from src.infra.adapter.repository.redis.repository_config import get_stream_redis_client

logging.basicConfig(level=logging.INFO)
redis_client = get_stream_redis_client()
load_dotenv()

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars("file:///jars/flink-sql-connector-kafka-3.0.1-1.18.jar")

kafka_producer_dlq = FlinkKafkaProducer(
    topic=os.getenv("KAFKA_CUSTOMER_PRODUCT_DLQ_TOPIC"),
    serialization_schema=SimpleStringSchema(),
    producer_config={"bootstrap.servers": os.getenv("KAFKA_CUSTOMER_PRODUCT_SERVERS")},
)


def write_data_to_redis(
    key: str, value: Any, customer_id: str = None, product_id: str = None
):
    retries = 5
    retry_delay = 2  # seconds
    retry_count = 0
    while retries > 0:
        try:
            # Use a transaction or atomic operation
            with redis_client.pipeline() as pipe:
                pipe.multi()
                pipe.set(key, value)
                pipe.execute()
            break
        except redis.RedisError as e:
            retries -= 1
            time.sleep(1)  # Optional: backoff before retrying
            logging.warning(f"Retry {retry_count + 1} failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            if retries == 0:
                error_message = json.dumps(
                    {
                        "key": key,
                        "value": value,
                        "customer_id": customer_id,
                        "product_id": product_id,
                        "error": str(e),
                    }
                )
                kafka_producer_dlq.send(error_message)
                # Optionally log the error or handle it further
                logging.error(f"Error writing to Redis: {error_message}")
