import asyncio
from fastapi import APIRouter, HTTPException, Query

from app.services.waqi import get_waqi
from app.services.openaq import get_openaq
from app.services.processing import normalize_waqi, normalize_openaq

router = APIRouter(prefix="/air-quality", tags=["Air Quality"])


@router.get("")
async def current_air_quality(
    lat: float = Query(ge=-90, le=90),
    lon: float = Query(ge=-180, le=180),
):
    # ask both services at the same time
    waqi_raw, openaq_raw = await asyncio.gather(
        get_waqi(lat, lon), get_openaq(lat, lon)
    )
    waqi = normalize_waqi(waqi_raw)
    openaq = normalize_openaq(openaq_raw)

    if not waqi and not openaq:
        raise HTTPException(
            status_code=503,
            detail="No air quality data available near this location right now.",
        )

    primary = waqi or openaq
    # fill gaps in pollutants using the other source
    pollutants = dict(primary["pollutants"])
    other = openaq if primary is waqi else waqi
    if other:
        for p, val in other["pollutants"].items():
            if pollutants.get(p) is None and val is not None:
                pollutants[p] = val

    return {
        "location": {"lat": lat, "lon": lon},
        "aqi": primary["aqi"] if primary["aqi"] is not None else (waqi or {}).get("aqi"),
        "pollutants": pollutants,
        "station": {
            "name": primary["station"],
            "lat": primary["station_lat"],
            "lon": primary["station_lon"],
        },
        "sources_used": [s["source"] for s in (waqi, openaq) if s],
        "timestamp": primary["timestamp"],
    }