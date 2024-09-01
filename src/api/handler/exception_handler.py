import traceback
from typing import Dict, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.api.handler.error_response import ErrorResponse
from src.infra.config.logging_config import get_logger
from src.infra.exception.bad_request_exception import BadRequestException
from src.infra.exception.forbidden_exception import ForbiddenException
from src.infra.exception.infra_exception import InfraException
from src.infra.exception.not_found_exception import NotFoundException
from src.infra.util.errors import errors

logger = get_logger()


def unhandled_exception_handler(request, exc: Exception):
    error_code = 1999
    logger.error(generate_error_message(error_code))
    logger.error(generate_stack_trace(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=generate_error_content(error_code=error_code),
    )


def http_exception_handler_manual(exc: HTTPException):
    error_code = 1999

    if status.HTTP_401_UNAUTHORIZED == exc.status_code:
        error_code = 1200

    if status.HTTP_403_FORBIDDEN == exc.status_code:
        error_code = 1201

    if status.HTTP_422_UNPROCESSABLE_ENTITY == exc.status_code:
        error_code = 1999

    logger.error(generate_error_message(error_code), exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            ErrorResponse(
                error_code=error_code, error_message=str(exc.detail)
            ).model_dump()
        ),
    )


def http_exception_handler(request, exc: HTTPException):
    error_code = 1999

    if status.HTTP_401_UNAUTHORIZED == exc.status_code:
        error_code = 1200

    if status.HTTP_403_FORBIDDEN == exc.status_code:
        error_code = 1201

    if status.HTTP_404_NOT_FOUND == exc.status_code:
        error_code = 1000

    is_logged = False
    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.critical(
            generate_error_message(error_code) + " | " + generate_stack_trace(exc)
        )
        is_logged = True

    if exc.status_code >= status.HTTP_400_BAD_REQUEST and not is_logged:
        logger.info(generate_error_message(error_code))

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            ErrorResponse(
                error_code=error_code, error_message=errors[error_code]
            ).model_dump()
        ),
    )


def validation_exception_handler(request, exc: RequestValidationError):
    error_code = 1000
    logger.error(msg=generate_error_message(error_code))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=generate_error_content(
            error_code=error_code, error_detail=exc.errors()
        ),
    )


def not_found_exception_handler(request, exc: NotFoundException):
    logger.error(generate_error_message(exc.error_code))
    return generate_json_response(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code=exc.error_code,
        error_detail=exc.error_detail,
    )


def bad_request_exception_handler(request, exc: BadRequestException):
    logger.error(
        generate_error_message(exc.error_code),
    )
    logger.error(
        generate_stack_trace(exc.cause_exception)
        if exc.cause_exception is not None
        else "",
    )
    return generate_json_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code=exc.error_code,
        error_detail=exc.error_detail,
    )


async def forbidden_exception_handler(request, exc: ForbiddenException):
    logger.warning(
        generate_error_message(exc.error_code)
        + " | "
        + (
            generate_stack_trace(exc.cause_exception)
            if exc.cause_exception is not None
            else ""
        )
    )

    return generate_json_response(
        status_code=status.HTTP_403_FORBIDDEN,
        error_code=exc.error_code,
        error_detail=exc.error_detail,
    )


async def connection_exception_handler(request, exc: ForbiddenException):
    logger.error(
        generate_error_message(exc.error_code)
        + " | "
        + (
            generate_stack_trace(exc.cause_exception)
            if exc.cause_exception is not None
            else ""
        )
    )

    return generate_json_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        error_code=exc.error_code,
        error_detail=exc.error_detail,
    )


def infra_exception_handler(request, exc: InfraException):
    logger.error(
        generate_error_message(exc.error_code),
    )
    logger.error(
        generate_stack_trace(exc.cause_exception)
        if exc.cause_exception is not None
        else "",
    )
    return generate_json_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code=exc.error_code,
        error_detail=exc.error_detail,
    )


def generate_json_response(
    status_code: int, error_code: int, error_detail: Optional[Dict]
):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            ErrorResponse(
                error_code=error_code,
                error_message=errors[error_code],
                error_detail=[error_detail] if error_detail else None,
            ).model_dump()
        ),
    )


def generate_error_message(error_code):
    return "error code: {}, error message: {}".format(error_code, errors[error_code])


def generate_stack_trace(exc: Exception) -> str:
    return "".join(traceback.TracebackException.from_exception(exc).format())


def generate_error_content(error_code: int, error_detail: list = []):
    return jsonable_encoder(
        ErrorResponse(
            error_code=error_code,
            error_message=errors[error_code],
            error_detail=error_detail,
        ).model_dump()
    )
