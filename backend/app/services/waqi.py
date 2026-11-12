import httpx
from app.core import config

POLLUTANTS = ["pm25", "pm10", "no2", "o3", "co"]


async def get_waqi(lat: float, lon: float) -> dict | None:
    """Returns raw-ish WAQI data, or None if unavailable."""
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params={"token": config.WAQI_TOKEN})
            resp.raise_for_status()
    except (httpx.TimeoutException, httpx.HTTPError):
        return None

    body = resp.json()
    if body.get("status") != "ok":
        return None  # wrong token, or no station nearby

    d = body["data"]
    iaqi = d.get("iaqi", {})

    return {
        "source": "WAQI",
        "aqi": d.get("aqi"),                      # can be "-" if unavailable
        "station": d.get("city", {}).get("name"),
        "station_lat": (d.get("city", {}).get("geo") or [None, None])[0],
        "station_lon": (d.get("city", {}).get("geo") or [None, None])[1],
        "time": d.get("time", {}).get("iso"),
        "pollutants": {p: iaqi[p]["v"] for p in POLLUTANTS if p in iaqi},
    }