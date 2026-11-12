from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class LocationResponse(Location):
    received_at: datetime