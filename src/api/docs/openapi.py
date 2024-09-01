import json
from typing import List

from src.api.handler.error_response import ErrorResponse
from src.infra.util.errors import errors


def generate_unprocessable_entity_error_response(error_code=1100):
    return {
        "application/json": {
            "example": json.dumps(
                ErrorResponse(
                    error_code=error_code, error_message=errors[error_code]
                ).dict()
            )
        }
    }


def generate_error_detail(error_location: List[str]):
    return [
        {"loc": error_location, "msg": "field required", "type": "value_error.missing"}
    ]


def generate_validation_error_response(
    invalid_field_location: List[str] = ["body", "device_id"]
):
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
