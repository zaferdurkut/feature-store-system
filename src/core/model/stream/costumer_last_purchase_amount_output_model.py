from pydantic import BaseModel


class CustomerLastPurchaseAmountOutputModel(BaseModel):
    amount: float
