from pydantic import BaseModel, Field


class LastMonthCategoryRevenueOutputDto(BaseModel):
    revenue: float = Field(..., description='Revenue of the category', examples=[1000.0])
