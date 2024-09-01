from typing import Tuple

from pyflink.common.typeinfo import Types
from pyflink.datastream import MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from consumer.redis_adapter import write_data_to_redis


# MapFunction to create a tuple (ProductID, ReviewRating)
class ReviewMapFunction(MapFunction):
    def map(self, value: dict) -> Tuple[str, float]:

        return value["ProductID"], value["ReviewRating"]


class CalculateAverageAndWriteToRedis(MapFunction):
    def __init__(self):
        self.reviews_state = None

    def open(self, runtime_context):
        state_descriptor = ValueStateDescriptor(
            "last_5_reviews", Types.LIST(Types.FLOAT())
        )
        self.reviews_state = runtime_context.get_state(state_descriptor)

    def map(self, value: Tuple[str, float]) -> str:
        product_id, review_rating = value

        # Retrieve current state
        current_reviews = self.reviews_state.value()
        if current_reviews is None:
            current_reviews = []

        # Update the list with the new review
        current_reviews.append(review_rating)
        if len(current_reviews) > 5:
            current_reviews.pop(
                0
            )  # Remove the oldest review to keep only the last 5, FIFO

        # Update the state
        self.reviews_state.update(current_reviews)

        # Calculate the average of the last 5 reviews
        avg_review = sum(current_reviews) / len(current_reviews)

        # Store the result in Redis
        write_data_to_redis(
            key=f"avg_review:{product_id}", value=avg_review, product_id=product_id
        )

        return f"avg_review: ProductID: {product_id}, AvgReview: {avg_review}"
