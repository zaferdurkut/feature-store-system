import json
from typing import Tuple

from pyflink.common.typeinfo import Types
from pyflink.datastream import MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from consumer.redis_adapter import write_data_to_redis


# MapFunction to create a tuple (CustomerID, ProductID, ReviewRating)
class CustomerProductReviewMapFunction(MapFunction):
    def map(self, value: dict) -> Tuple[str, str, float]:
        return value["CustomerID"], value["ProductID"], value["ReviewRating"]


class CalculateCustomerProductLastReviewAndWriteToRedis(MapFunction):
    def __init__(self):
        self.last_review_state = None

    def open(self, runtime_context):
        # Define state to store the latest review rating for each customer-product pair
        state_descriptor = ValueStateDescriptor("last_review_rating", Types.FLOAT())
        self.last_review_state = runtime_context.get_state(state_descriptor)

    def map(self, value: Tuple[str, str, float]) -> str:
        customer_id, product_id, review_rating = value

        self.last_review_state.update(review_rating)
        latest_review_rating = self.last_review_state.value()

        # Use a composite key for state: (CustomerID, ProductID)
        key = f"{customer_id}_{product_id}"

        write_data_to_redis(
            key=f"last_review:{key}",
            value=latest_review_rating,
            customer_id=customer_id,
            product_id=product_id,
        )

        return f"last_review: CustomerID: {customer_id}, ProductID: {product_id}, LastReviewRating: {latest_review_rating}"
