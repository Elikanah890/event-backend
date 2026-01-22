from datetime import datetime

def utc_now() -> datetime:
    return datetime.utcnow()

def is_event_active(start_time: datetime, end_time: datetime) -> bool:
    """
    Check if event is currently active.
    """
    now = utc_now()
    return start_time <= now <= end_time
