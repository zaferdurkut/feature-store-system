import json
import logging
import os
import random
from time import sleep
from dotenv import load_dotenv

import pandas as pd
from kafka import KafkaProducer
from pandas import DataFrame

logging.basicConfig(level=logging.INFO)
load_dotenv()


class CustomerProductProducer:
    """Push Kafka for messages and write to Cassandra."""

    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_CUSTOMER_PRODUCT_SERVERS"),
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        self.topic = os.getenv("KAFKA_CUSTOMER_PRODUCT_TOPIC")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kafka_producer.flush()

    def main(self) -> None:
        click_dataframe = self.read_csv()
        while True:
            for item in click_dataframe.to_dict(orient="records"):
                sleep(round(random.uniform(0.1,1.2),2))
                self.send(topic=self.topic, item=item)
            sleep(2)
            logging.info("All Dataframe data sent to Kafka. After 2 seconds, it will send again.")

    def send(self, topic: str, item: dict) -> None:
        """Connect to Kafka and  push message to Topic"""

        self.kafka_producer.send(topic=topic, value=item).add_callback(
            CustomerProductProducer.on_send_success
        ).add_errback(CustomerProductProducer.on_send_error)

    @staticmethod
    def on_send_success(record_metadata):
        logging.info(
            "Topic: "
            + str(record_metadata.topic)
            + " Partition: "
            + str(record_metadata.partition)
            + " Offset: "
            + str(record_metadata.offset)
            + " Timestamp: "
            + str(record_metadata.timestamp)

        )

    @staticmethod
    def on_send_error(excp):
        logging.error(excp)


    def read_csv(self) -> DataFrame:
        return pd.read_csv("./data/ecommerce_transactions.csv")


if __name__ == "__main__":
    CustomerProductProducer().main()
