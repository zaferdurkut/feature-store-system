from pydantic import BaseModel


class LastMonthSoldProductUnitsOutputModel(BaseModel):
    units : int
