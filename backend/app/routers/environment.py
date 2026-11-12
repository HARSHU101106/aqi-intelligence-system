from fastapi import APIRouter, HTTPException, Query
from app.services.aggregator import get_environment
from app.services.storage import save_environment

router = APIRouter(tags=["environment"])

@router.get("/environment")
async def environment(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    save: bool = True,
):
    data = await get_environment(lat, lon)

    if not any(data["sources_available"].values()):
        raise HTTPException(
            status_code=503,
            detail="No environmental data providers are reachable right now. Try again later.",
        )

    if save:
        save_environment(data)

    return data