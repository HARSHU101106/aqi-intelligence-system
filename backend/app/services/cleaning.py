from datetime import datetime, timezone

# Realistic min/max for each value. Anything outside is a sensor error.
VALID_RANGES = {
    "pm25": (0, 1000),
    "pm10": (0, 2000),
    "no2": (0, 2000),
    "o3": (0, 1000),
    "co": (0, 50000),
    "temperature_c": (-60, 60),
    "humidity_pct": (0, 100),
    "pressure_hpa": (800, 1100),
    "wind_speed_ms": (0, 100),
    "rainfall_mm": (0, 500),
    "congestion_index": (0, 1),
}

# Convert ppb to ug/m3 at 25C: ug/m3 = ppb * molecular_weight / 24.45
MOLECULAR_WEIGHT = {"no2": 46.01, "o3": 48.00, "co": 28.01}

def to_ugm3(pollutant: str, value: float, unit: str):
    """Make every pollutant use the same unit (ug/m3)."""
    unit = (unit or "").lower().replace("µ", "u")
    if unit in ("ug/m3", "ugm3", "µg/m³"):
        return value
    if unit == "ppb" and pollutant in MOLECULAR_WEIGHT:
        return round(value * MOLECULAR_WEIGHT[pollutant] / 24.45, 2)
    if unit == "ppm" and pollutant in MOLECULAR_WEIGHT:
        return round(value * 1000 * MOLECULAR_WEIGHT[pollutant] / 24.45, 2)
    return None   # unknown unit: do not guess

def is_valid(name: str, value) -> bool:
    if value is None:
        return False
    low, high = VALID_RANGES.get(name, (float("-inf"), float("inf")))
    return low <= value <= high

def clean_dict(data: dict) -> dict:
    """Keep only valid numbers, set bad ones to None."""
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            cleaned[key] = value if is_valid(key, value) else None
        else:
            cleaned[key] = value
    return cleaned

def normalize_timestamp(ts) -> str:
    """Return the time in UTC ISO format. Fall back to now."""
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()