import chromadb
from chromadb.config import Settings as ChromaSettings
import structlog
import redis as redis_client

from backend.core.config import settings

logger = structlog.get_logger()

async def check_chromadb() -> dict:
    try:
        client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        client.heartbeat()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_redis() -> dict:
    try:
        r = redis_client.from_url(settings.REDIS_URL)
        r.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_groq() -> dict:
    try:
        from groq import Groq
        client = Groq(api_key=settings.GROQ_API_KEY)
        client.models.list()
        return {"status": "healthy", "model": settings.GROQ_MODEL}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def get_full_health() -> dict:
    chroma = await check_chromadb()
    red    = await check_redis()
    groq   = await check_groq()

    all_healthy = all(
        s["status"] == "healthy"
        for s in [chroma, red, groq]
    )

    return {
        "status":   "healthy" if all_healthy else "degraded",
        "services": {
            "chromadb": chroma,
            "redis":    red,
            "groq":     groq,
        },
    }