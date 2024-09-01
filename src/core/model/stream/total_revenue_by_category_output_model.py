from pydantic import BaseModel


class TotalRevenueByCategoryOutputModel(BaseModel):
    revenue: float
