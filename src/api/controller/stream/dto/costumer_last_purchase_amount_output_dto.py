from pydantic import BaseModel, Field


class CustomerLastPurchaseAmountOutputDto(BaseModel):
    amount: int = Field(..., description="The amount of the last purchase", examples=[10, 200])
