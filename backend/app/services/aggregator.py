import asyncio
from app.services.waqi import get_waqi
from app.services.weather import get_weather
from app.services.traffic import get_traffic
from app.services.cleaning import clean_dict, normalize_timestamp
# from app.services.openaq import get_openaq   # use your Day 3 function

async def get_environment(lat: float, lon: float):
    # Ask all services AT THE SAME TIME
    aq, weather, traffic = await asyncio.gather(
        get_waqi(lat, lon),
        get_weather(lat, lon),
        get_traffic(lat, lon),
    )

    air = None
    if aq:
        air = {
            "aqi": aq.get("aqi"),
            "station": aq.get("station"),
            "source": "WAQI",
            "pollutants": clean_dict(aq.get("pollutants", {})),
        }

    result = {
        "location": {"lat": lat, "lon": lon},
        "air_quality": air,
        "weather": clean_dict(weather) if weather else None,
        "traffic": clean_dict(traffic) if traffic else None,
        "timestamp": normalize_timestamp(aq.get("time") if aq else None),
        "sources_available": {
            "air_quality": air is not None,
            "weather": weather is not None,
            "traffic": traffic is not None,
        },
    }
    return result