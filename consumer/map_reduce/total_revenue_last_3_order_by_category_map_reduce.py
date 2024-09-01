import json
from typing import Tuple

from pyflink.common.typeinfo import Types
from pyflink.datastream import MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from consumer.redis_adapter import write_data_to_redis


# MapFunction to create a tuple (Category, Revenue)
class OrderMapFunction(MapFunction):
    def map(self, value: dict) -> Tuple[str, float]:
        return value["Category"], value["Price"] * value["Quantity"]


class CalculateRevenueAndWriteToRedis(MapFunction):
    def __init__(self):
        self.orders_state = None

    def open(self, runtime_context):
        # Define state to store the last 3 orders
        state_descriptor = ValueStateDescriptor(
            "last_3_orders", Types.LIST(Types.FLOAT())
        )
        self.orders_state = runtime_context.get_state(state_descriptor)

    def map(self, value: Tuple[str, float]) -> str:
        category, revenue = value

        # Retrieve current state
        current_orders = self.orders_state.value()
        if current_orders is None:
            current_orders = []

        # Update the list with the new order revenue
        current_orders.append(revenue)
        if len(current_orders) > 3:
            current_orders.pop(
                0
            )  # Remove the oldest order to keep only the last 3, FIFO

        self.orders_state.update(current_orders)

        # Calculate the total revenue of the last 3 orders
        total_revenue = sum(current_orders)

        # redis_client.set(f"revenue_category:{category}", total_revenue)
        write_data_to_redis(key=f"revenue_category:{category}", value=total_revenue )

        return f"revenue_category: Category: {category}, TotalRevenue: {total_revenue}"
