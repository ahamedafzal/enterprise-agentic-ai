import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env FIRST before any langchain imports
load_dotenv(Path(__file__).parent.parent / ".env")

# Force set LangSmith vars into os.environ immediately
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"]    = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"]    = os.getenv("LANGCHAIN_PROJECT", "enterprise-agentic-ai")
os.environ["LANGCHAIN_ENDPOINT"]   = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from backend.core.config import settings
from backend.api.routes import auth, workflow, agents, documents, websocket

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(workflow.router)
app.include_router(agents.router)
app.include_router(documents.router)
app.include_router(websocket.router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "name":    settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status":  "operational",
        "docs":    "/docs",
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}