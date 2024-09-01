from enum import Enum


class HealthCheckType(str, Enum):
    healthy = ("healthy",)
    fail = ("unhealthy",)
    warn = "healthy with some concerns"
