import logging
import os

from dotenv import load_dotenv
from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource

from consumer.schema import ParseAndValidate, CUSTOMER_PRODUCT_SCHEMA
from consumer.map_reduce.average_last_5_review_map_reduce import (
    ReviewMapFunction,
    CalculateAverageAndWriteToRedis,
)
from consumer.map_reduce.customer_last_order_amount_map_reduce import (
    CalculateLastPurchaseAndWriteToRedis,
    CustomerOrderAmountMapFunction,
)
from consumer.map_reduce.customer_product_review_rating_map_reduce import (
    CustomerProductReviewMapFunction,
    CalculateCustomerProductLastReviewAndWriteToRedis,
)
from consumer.map_reduce.total_revenue_last_3_order_by_category_map_reduce import (
    OrderMapFunction,
    CalculateRevenueAndWriteToRedis,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()


def main():
    # # Configure RocksDBStateBackend
    # state_backend = RocksDBStateBackend(
    #     'file:///tmp/flink-checkpoints',
    #     incremental=True
    # )
    # env.set_state_backend(state_backend)

    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///jars/flink-sql-connector-kafka-3.0.1-1.18.jar")

    kafka_source = (
        KafkaSource.builder()
        .set_bootstrap_servers(os.getenv("KAFKA_CUSTOMER_PRODUCT_SERVERS"))
        .set_topics(os.getenv("KAFKA_CUSTOMER_PRODUCT_TOPIC"))
        .set_group_id("flink_group")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    # Create a data stream from the Kafka source
    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka Source"
    )

    # Last 5 Product Review Average
    last_5_review_average_stream = (
        data_stream
        .map(ParseAndValidate(), output_type=CUSTOMER_PRODUCT_SCHEMA)
        .map(
            ReviewMapFunction(),
            output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()]),
        )  # Map JSON to (ProductID, ReviewRating)
        .key_by(lambda x: x[0])  # Key by ProductID
        .map(CalculateAverageAndWriteToRedis(), output_type=Types.STRING())
    )
    last_5_review_average_stream.print()

    # Last 3 Order Revenue by Category
    last_3_order_revenue_stream = (
        data_stream
        .map(ParseAndValidate(), output_type=CUSTOMER_PRODUCT_SCHEMA)
        .map(
            OrderMapFunction(), output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()])
        )  # Map JSON to (Category, Revenue)
        .key_by(lambda x: x[0])  # Key by Category
        .map(CalculateRevenueAndWriteToRedis(), output_type=Types.STRING())
    )
    last_3_order_revenue_stream.print()

    # Last Purchase Amount by Customer
    customer_last_order_amount_stream = (
        data_stream
        .map(ParseAndValidate(), output_type=CUSTOMER_PRODUCT_SCHEMA)
        .map(
            CustomerOrderAmountMapFunction(),
            output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()]),
        )  # Map JSON to (CustomerID, AmountPaid)
        .key_by(lambda x: x[0])  # Key by CustomerID
        .map(CalculateLastPurchaseAndWriteToRedis(), output_type=Types.STRING())
    )
    customer_last_order_amount_stream.print()

    # Customer Product Review Rating
    customer_last_review_rating_stream = (
        data_stream
        .map(ParseAndValidate(), output_type=CUSTOMER_PRODUCT_SCHEMA)
        .map(
            CustomerProductReviewMapFunction(),
            output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.FLOAT()]),
        )  # Map JSON to (CustomerID, ProductID, ReviewRating)
        .key_by(lambda x: (x[0], x[1]))  # Key by (CustomerID, ProductID)
        .map(
            CalculateCustomerProductLastReviewAndWriteToRedis(),
            output_type=Types.STRING(),
        )
    )
    customer_last_review_rating_stream.print()

    # Execute the program
    env.execute("Flink Customer Product Stream Consumer")


if __name__ == "__main__":
    main()
