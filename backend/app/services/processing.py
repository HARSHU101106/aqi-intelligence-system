from datetime import datetime, timezone

POLLUTANTS = ["pm25", "pm10", "no2", "o3", "co"]


def to_utc_iso(ts: str | None) -> str | None:
    """Turn any timestamp into UTC ISO format."""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def clean_aqi(value) -> int | None:
    """WAQI sometimes sends '-' instead of a number."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return int(v) if 0 <= v <= 500 else None


def clean_value(value) -> float | None:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return v if v >= 0 else None          # negative concentration = sensor error


def normalize_waqi(raw: dict | None) -> dict | None:
    if not raw:
        return None
    pollutants = {}
    for p in POLLUTANTS:
        v = clean_value(raw["pollutants"].get(p))
        # WAQI gives index values (sub-AQI), not raw concentrations
        pollutants[p] = {"value": v, "unit": "AQI index"} if v is not None else None
    return {
        "source": "WAQI",
        "aqi": clean_aqi(raw.get("aqi")),
        "station": raw.get("station"),
        "station_lat": raw.get("station_lat"),
        "station_lon": raw.get("station_lon"),
        "timestamp": to_utc_iso(raw.get("time")),
        "pollutants": pollutants,
    }


def normalize_openaq(raw: dict | None) -> dict | None:
    if not raw:
        return None
    pollutants = {}
    for p in POLLUTANTS:
        item = raw["pollutants"].get(p)
        v = clean_value(item["value"]) if item else None
        pollutants[p] = {"value": v, "unit": item["unit"]} if v is not None else None
    return {
        "source": "OpenAQ",
        "aqi": None,
        "station": raw.get("station"),
        "station_lat": raw.get("station_lat"),
        "station_lon": raw.get("station_lon"),
        "timestamp": to_utc_iso(raw.get("time")),
        "pollutants": pollutants,
    }