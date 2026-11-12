import httpx
from app.core import config

BASE = "https://api.openaq.org/v3"
WANTED = {"pm25", "pm10", "no2", "o3", "co"}


async def get_openaq(lat: float, lon: float) -> dict | None:
    headers = {"X-API-Key": config.OPENAQ_API_KEY or ""}

    try:
        async with httpx.AsyncClient(timeout=15, headers=headers) as client:
            # Step 1: find nearby stations
            r = await client.get(
                f"{BASE}/locations",
                params={"coordinates": f"{lat},{lon}", "radius": 25000, "limit": 5},
            )
            r.raise_for_status()
            stations = r.json().get("results", [])

            # Step 2: try stations in order until one has fresh readings
            for st in stations:
                # Map sensor id -> (pollutant name, unit)
                sensor_map = {}
                for s in st.get("sensors", []):
                    param = s.get("parameter", {})
                    sensor_map[s["id"]] = (param.get("name"), param.get("units"))

                lr = await client.get(f"{BASE}/locations/{st['id']}/latest")
                if lr.status_code != 200:
                    continue

                pollutants = {}
                latest_time = None
                for item in lr.json().get("results", []):
                    name, unit = sensor_map.get(item.get("sensorsId"), (None, None))
                    if name in WANTED:
                        pollutants[name] = {"value": item.get("value"), "unit": unit}
                        t = (item.get("datetime") or {}).get("utc")
                        if t and (latest_time is None or t > latest_time):
                            latest_time = t

                if pollutants:
                    coords = st.get("coordinates") or {}
                    return {
                        "source": "OpenAQ",
                        "station": st.get("name"),
                        "station_lat": coords.get("latitude"),
                        "station_lon": coords.get("longitude"),
                        "time": latest_time,
                        "pollutants": pollutants,
                    }
    except (httpx.TimeoutException, httpx.HTTPError):
        return None

    return None