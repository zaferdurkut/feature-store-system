from fastapi import APIRouter
from starlette import status

from src.api.controller.health_check.dto.health_check_output_dto import (
    HealthCheckOutputDto,
)
from src.infra.util.enum import HealthCheckType

router = APIRouter()


@router.get(
    "/health-check",
    response_model=HealthCheckOutputDto,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": HealthCheckOutputDto}},
)
async def health_check():
    return HealthCheckOutputDto(status=HealthCheckType.healthy.value)
