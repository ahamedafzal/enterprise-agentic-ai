import uuid
import time
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.core.logging import bind_trace_id

logger = structlog.get_logger()

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id   = str(uuid.uuid4())[:8]
        start_time = time.time()

        bind_trace_id(trace_id)

        response = await call_next(request)

        duration_ms = round((time.time() - start_time) * 1000)
        logger.info(
            "Request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration_ms,
            trace_id=trace_id,
        )

        response.headers["X-Trace-ID"] = trace_id
        return response