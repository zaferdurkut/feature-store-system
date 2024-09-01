from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.api.controller.health_check import health_check_controller
from src.api.controller.auth import auth_controller
from src.api.controller.stream import stream_controller
from src.api.controller.offline import offline_controller
from src.api.handler.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
    not_found_exception_handler,
    infra_exception_handler,
    bad_request_exception_handler,
    forbidden_exception_handler,
    connection_exception_handler,
)
from src.api.middleware.request_response_middleware import RequestResponseMiddleware
from src.infra.exception.bad_request_exception import BadRequestException
from src.infra.exception.connection_exception import ConnectionException
from src.infra.exception.forbidden_exception import ForbiddenException
from src.infra.exception.infra_exception import InfraException
from src.infra.exception.not_found_exception import NotFoundException


def create_app():
    app = FastAPI(
        title="Feature Store API",
        description="The API for Feature Store Service",
        version="0.1.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc",
    )

    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(InfraException, infra_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    app.add_exception_handler(ConnectionException, connection_exception_handler)
    app.add_middleware(RequestResponseMiddleware)

    app.include_router(
        health_check_controller.router, prefix="/api", tags=["health check"]
    )

    app.include_router(auth_controller.router, prefix="/api/auth", tags=["auth"])

    app.include_router(
        stream_controller.router,
        prefix="/api/v1/stream",
        tags=["stream"],
    )

    app.include_router(
        offline_controller.router,
        prefix="/api/v1/offline",
        tags=["offline"],
    )

    return app
