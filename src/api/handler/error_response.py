from typing import Optional, List, Any

from pydantic.main import BaseModel

from src.infra.util.errors import errors


def generate_error_response():
    return {
        "application/json": {
            "example": ErrorResponse(
                error_code=10, error_message="Cannot get expected response"
            ).dict()
        }
    }


def generate_validation_error_response(invalid_field_location: List[str]):
    return {
        "application/json": {
            "example": ErrorResponse(
                error_code=1000,
                error_message=errors[1000],
                error_detail=generate_error_detail(
                    error_location=invalid_field_location
                ),
            ).dict()
        }
    }


def generate_error_detail(error_location: List[str]):
    return [
        {
            "loc": error_location,
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


class ErrorResponse(BaseModel):
    error_code: Optional[int] = None
    error_message: Optional[str] = None
    error_detail: Optional[list] = None
