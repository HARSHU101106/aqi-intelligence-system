from fastapi import APIRouter, HTTPException
from influxdb_client import Point
from pydantic import EmailStr

from app.core import config
from app.db.influx import write_api, query_api
from app.schemas.user import UserCreate, UserResponse, HealthProfile
from app.services.health import get_default_threshold

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    h = user.health

    # use the user's own number, or calculate a default
    if h.alert_threshold_aqi is not None:
        threshold = h.alert_threshold_aqi
    else:
        threshold = get_default_threshold(h)

    point = (
        Point("user_profiles")
        .tag("email", user.email.lower())
        .field("name", user.name)
        .field("asthmatic", h.asthmatic)
        .field("elderly", h.elderly)
        .field("child", h.child)
        .field("alert_threshold_aqi", threshold)
    )

    try:
        write_api.write(bucket=config.INFLUX_BUCKET, record=point)
    except Exception:
        raise HTTPException(status_code=503, detail="Database is not available")

    return UserResponse(
        name=user.name,
        email=user.email,
        health=HealthProfile(
            asthmatic=h.asthmatic,
            elderly=h.elderly,
            child=h.child,
            alert_threshold_aqi=threshold,
        ),
    )


@router.get("/{email}", response_model=UserResponse)
def get_user(email: EmailStr):
    email = email.lower()
    if '"' in email:
        raise HTTPException(status_code=400, detail="Invalid email")

    flux = f'''
    from(bucket: "{config.INFLUX_BUCKET}")
      |> range(start: -365d)
      |> filter(fn: (r) => r._measurement == "user_profiles" and r.email == "{email}")
      |> last()
      |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''

    try:
        tables = query_api.query(flux)
    except Exception:
        raise HTTPException(status_code=503, detail="Database is not available")

    records = [rec for table in tables for rec in table.records]
    if not records:
        raise HTTPException(status_code=404, detail="User not found")

    r = records[0].values
    return UserResponse(
        name=r["name"],
        email=email,
        health=HealthProfile(
            asthmatic=r["asthmatic"],
            elderly=r["elderly"],
            child=r["child"],
            alert_threshold_aqi=int(r["alert_threshold_aqi"]),
        ),
    )