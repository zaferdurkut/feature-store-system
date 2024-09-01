from pydantic import BaseModel


class LastMonthCategoryRevenueOutputModel(BaseModel):
    revenue: float
