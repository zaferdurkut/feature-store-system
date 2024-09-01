from pydantic import BaseModel, Field

from src.infra.util.enum import HealthCheckType


class HealthCheckOutputDto(BaseModel):
    status: str = Field(default=HealthCheckType.healthy.value, example="healthy")
