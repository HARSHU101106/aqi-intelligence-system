from app.schemas.user import HealthProfile


def get_default_threshold(health: HealthProfile) -> int:
    """Pick a safe AQI alert level. The most sensitive condition wins."""
    threshold = 150          # healthy adult
    if health.elderly or health.child:
        threshold = 100
    if health.asthmatic:
        threshold = 75
    return threshold