import httpx
from app.core import config

async def get_traffic(lat: float, lon: float):
    if not config.TOMTOM_API_KEY:
        return None

    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {"point": f"{lat},{lon}", "key": config.TOMTOM_API_KEY}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
        if r.status_code != 200:
            return None
        seg = r.json().get("flowSegmentData", {})
    except (httpx.TimeoutException, httpx.RequestError):
        return None

    current = seg.get("currentSpeed")
    free = seg.get("freeFlowSpeed")
    if not current or not free:
        return None

    # 0 = empty road, 1 = completely jammed
    congestion = max(0.0, min(1.0, 1 - current / free))

    return {
        "current_speed_kmh": current,
        "free_flow_speed_kmh": free,
        "congestion_index": round(congestion, 2),
        "road_closure": seg.get("roadClosure", False),
    }