from pydantic import BaseModel, Field


class TotalRevenueByCategoryOutputDto(BaseModel):
    revenue: float = Field(..., description="The total revenue of the category", examples=[10.5, 200.5])
