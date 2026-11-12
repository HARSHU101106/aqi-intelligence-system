import httpx
from app.core import config

async def get_weather(lat: float, lon: float):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": config.OPENWEATHER_API_KEY,
        "units": "metric",   # Celsius, m/s
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
        if r.status_code != 200:
            return None
        d = r.json()
    except (httpx.TimeoutException, httpx.RequestError):
        return None

    return {
        "temperature_c": d.get("main", {}).get("temp"),
        "humidity_pct": d.get("main", {}).get("humidity"),
        "pressure_hpa": d.get("main", {}).get("pressure"),
        "wind_speed_ms": d.get("wind", {}).get("speed"),
        "rainfall_mm": d.get("rain", {}).get("1h", 0),   # 0 if no rain
        "condition": (d.get("weather") or [{}])[0].get("description"),
    }