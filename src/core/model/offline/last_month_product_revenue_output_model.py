from pydantic import BaseModel


class LastMonthProductRevenueOutputModel(BaseModel):
    revenue: float
