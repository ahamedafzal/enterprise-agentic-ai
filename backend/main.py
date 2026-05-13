import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"]    = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"]    = os.getenv("LANGCHAIN_PROJECT", "enterprise-agentic-ai")
os.environ["LANGCHAIN_ENDPOINT"]   = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402
from prometheus_fastapi_instrumentator import Instrumentator  # noqa: E402
import structlog  # noqa: E402

from backend.core.config import settings  # noqa: E402
from backend.core.logging import setup_logging  # noqa: E402
from backend.core.middleware import TraceMiddleware  # noqa: E402
from backend.api.routes import auth, workflow, agents, documents, websocket, health  # noqa: E402

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting NEXUS", version=settings.APP_VERSION)
    yield
    logger.info("Shutting down NEXUS")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade multi-agent AI workflow system",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middlewares
app.add_middleware(TraceMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Routers
app.include_router(auth.router)
app.include_router(workflow.router)
app.include_router(agents.router)
app.include_router(documents.router)
app.include_router(websocket.router)
app.include_router(health.router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "name":    settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status":  "operational",
        "docs":    "/docs",
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}