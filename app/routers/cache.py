from fastapi import APIRouter

from app import cache

router = APIRouter(prefix="/api/v1/cache", tags=["cache"])


@router.get("/stats")
def cache_stats():
    return cache.stats()
