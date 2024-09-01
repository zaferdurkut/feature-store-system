import time
import uuid
from datetime import datetime

from fastapi import Request, Response

from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.config.logging_config import get_logger
from src.infra.util.constants import TRACE_ID_FIELD_NAME

LOG_MIDDLEWARE_IS_ENABLED = True
LOG_TRACE_ID_HEADER_NAME = "TRACE-ID"
LOG_IS_ENABLED = True
TRACE_ID_REF = None

logger = get_logger()


def setup_trace_id(ref):
    global TRACE_ID_REF
    TRACE_ID_REF = ref


class RequestResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        self.process_request(request)
        response = await call_next(request)
        self.process_response(request, response)
        return response

    @staticmethod
    def check_media_type(media_type: str):
        if media_type is not None and ("json" in media_type or "text" in media_type):
            return True
        return False

    @staticmethod
    def process_request(request: Request):
        if LOG_IS_ENABLED is not True:
            return

        if LOG_MIDDLEWARE_IS_ENABLED is True:
            request.state.start_time = time.time()

        def get_trace_id():
            if (
                LOG_TRACE_ID_HEADER_NAME in request.headers
                and request.headers[LOG_TRACE_ID_HEADER_NAME] is not None
            ):
                request.state.trace_id = request.headers[LOG_TRACE_ID_HEADER_NAME]
            elif TRACE_ID_FIELD_NAME not in request.state._state:
                request.state.trace_id = str(uuid.uuid1())

            return request.state.trace_id

        setup_trace_id(get_trace_id)
        return request

    @staticmethod
    def process_response(request: Request, response: Response):
        if LOG_IS_ENABLED is False or LOG_MIDDLEWARE_IS_ENABLED is False:
            return

        if b"content-length" in dict(response.raw_headers):
            data_len = str(dict(response.raw_headers)[b"content-length"], "utf-8")
        else:
            data_len = "-"

        elapsed_ms = int((time.time() - request.state.start_time) * 1000)
        http_status_code = response.status_code
        log_template = " {4} | {0} | {1} | {2} | {3}ms"

        if b"stream-agent" in dict(request.headers.raw):
            user_agent = str(dict(request.headers.raw)[b"stream-agent"], "utf-8")
        else:
            user_agent = "-"

        log_data = {
            "logger": "middleware",
            "remote_addr": request.client.host,
            "http_m": request.method,
            "uri": request.url.path,
            "http_s": http_status_code,
            "data_len": data_len,
            "user_agent": user_agent,
            "elapsed_ms": elapsed_ms,
        }

        if http_status_code >= 400:
            if http_status_code >= 500:
                logger.critical(
                    str.format(
                        log_template,
                        request.url.path,
                        request.method,
                        http_status_code,
                        elapsed_ms,
                        str(datetime.utcnow()),
                    ),
                    log_data,
                )
            else:
                logger.error(
                    str.format(
                        log_template,
                        request.url.path,
                        request.method,
                        http_status_code,
                        elapsed_ms,
                        datetime.utcnow(),
                    ),
                    log_data,
                )
        else:
            if str.endswith(request.url.path, "/health-check") is False:
                logger.info(
                    str.format(
                        log_template,
                        request.url.path,
                        request.method,
                        http_status_code,
                        elapsed_ms,
                        datetime.utcnow(),
                    ),
                    log_data,
                )
