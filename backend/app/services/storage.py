from datetime import datetime
from influxdb_client import Point, WritePrecision
from app.db.influx import write_api
from app.core import config

def save_environment(data: dict):
    lat = data["location"]["lat"]
    lon = data["location"]["lon"]
    ts = datetime.fromisoformat(data["timestamp"])

    station = (data.get("air_quality") or {}).get("station") or "unknown"

    point = (
        Point("environment")
        .tag("station", station)
        .tag("lat_lon", f"{round(lat, 3)},{round(lon, 3)}")
        .time(ts, WritePrecision.S)
    )

    def add(prefix_name, value):
        if value is not None and isinstance(value, (int, float)):
            point.field(prefix_name, float(value))

    air = data.get("air_quality") or {}
    add("aqi", air.get("aqi"))
    for name, val in (air.get("pollutants") or {}).items():
        add(name, val)

    for name, val in (data.get("weather") or {}).items():
        add(name, val)

    for name, val in (data.get("traffic") or {}).items():
        add(name, val)

    point.field("lat", float(lat)).field("lon", float(lon))

    write_api.write(bucket=config.INFLUX_BUCKET, record=point)