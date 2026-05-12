from fastapi import APIRouter
from backend.services.health_service import get_full_health

router = APIRouter(tags=["Health"])

@router.get("/health/detailed")
async def detailed_health():
    return await get_full_health()