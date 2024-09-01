from jaeger_client import Config
from opentracing.scope_managers import ThreadLocalScopeManager

from src.infra.config.app_config import (
    JAEGER_HOST,
    JAEGER_PORT,
    JAEGER_SAMPLER_TYPE,
    JAEGER_SAMPLER_RATE,
)
from src.infra.util.constants import APP_NAME

scope_manager = ThreadLocalScopeManager()


def init_tracer(service_name: str = APP_NAME):
    trace_id_header: str = "X-TRACE-ID"
    generate_128bit_trace_id: str = "1"
    config = Config(
        config={
            "local_agent": {
                "reporting_host": JAEGER_HOST,
                "reporting_port": JAEGER_PORT,
            },
            "sampler": {"type": JAEGER_SAMPLER_TYPE, "param": JAEGER_SAMPLER_RATE},
            "trace_id_header": trace_id_header,
            "generate_128bit_trace_id": generate_128bit_trace_id,
        },
        service_name=service_name,
        validate=True,
        scope_manager=scope_manager,
    )

    return config.initialize_tracer()


tracer = init_tracer(APP_NAME)
