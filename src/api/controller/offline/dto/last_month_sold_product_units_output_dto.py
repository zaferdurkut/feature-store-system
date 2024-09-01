from pydantic import BaseModel, Field


class LastMonthSoldProductUnitsOutputDto(BaseModel):
    units : int = Field(..., description="Number of units sold in the last month", examples=[100, 200, 300])
