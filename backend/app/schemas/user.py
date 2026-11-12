from pydantic import BaseModel, EmailStr, Field


class HealthProfile(BaseModel):
    asthmatic: bool = False
    elderly: bool = False
    child: bool = False
    # AQI number at which we should warn this user (optional)
    alert_threshold_aqi: int | None = Field(default=None, ge=0, le=500)


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    health: HealthProfile = HealthProfile()


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    health: HealthProfile