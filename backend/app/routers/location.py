from datetime import datetime, timezone
from fastapi import APIRouter
from app.schemas.location import Location, LocationResponse

router = APIRouter(prefix="/location", tags=["Location"])


@router.post("", response_model=LocationResponse)
def receive_location(loc: Location):
    return LocationResponse(
        lat=round(loc.lat, 5),
        lon=round(loc.lon, 5),
        received_at=datetime.now(timezone.utc),
    )