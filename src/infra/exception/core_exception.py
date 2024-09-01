from typing import Any

from src.infra.util.errors import errors


class CoreException(Exception):
    def __init__(
        self,
        error_code: int,
        error_detail: Any = None,
        cause_exception: Exception = None,
    ) -> None:
        super().__init__()
        self.error_message = errors[error_code]
        self.error_code = error_code
        self.error_detail = error_detail
        self.cause_exception = cause_exception
