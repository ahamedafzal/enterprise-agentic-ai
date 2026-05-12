import uuid
import structlog
from contextvars import ContextVar

# Context var to hold trace ID per request
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

def get_trace_id() -> str:
    return trace_id_var.get() or str(uuid.uuid4())[:8]

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

def bind_trace_id(trace_id: str):
    structlog.contextvars.bind_contextvars(trace_id=trace_id)
    trace_id_var.set(trace_id)