from pydantic import BaseModel, Field


class LastMonthProductRevenueOutputDto(BaseModel):
    revenue: float = Field(..., description="Revenue of the product", examples=[1000.0])
