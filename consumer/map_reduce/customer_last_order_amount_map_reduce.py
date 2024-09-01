import json
from typing import Tuple

from pyflink.common.typeinfo import Types
from pyflink.datastream import MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from consumer.redis_adapter import write_data_to_redis


# MapFunction to  create a tuple (CustomerID, AmountPaid)
class CustomerOrderAmountMapFunction(MapFunction):
    def map(self, value: dict) -> Tuple[str, float]:
        return value["CustomerID"], value["Price"]*value["Quantity"]


class CalculateLastPurchaseAndWriteToRedis(MapFunction):
    def __init__(self):
        self.last_purchase_state = None

    def open(self, runtime_context):
        # Define state to store the last purchase amount
        state_descriptor = ValueStateDescriptor("last_purchase_amount", Types.FLOAT())
        self.last_purchase_state = runtime_context.get_state(state_descriptor)

    def map(self, value: Tuple[str, float]) -> str:
        customer_id, amount_paid = value
        self.last_purchase_state.update(amount_paid)
        latest_amount_paid = self.last_purchase_state.value()

        write_data_to_redis(
            key=f"last_purchase_amount:{customer_id}",
            value=latest_amount_paid,
            customer_id=customer_id,
        )

        return f"last_purchase_amount: CustomerID: {customer_id}, LastPurchaseAmount: {latest_amount_paid}"
