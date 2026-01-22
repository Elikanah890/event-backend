from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.attendance import AttendanceLog
from app.models.invitation import Invitation
from app.models.guest import Guest
from typing import Dict

def get_event_summary(db: Session, event_id: int) -> Dict[str, int]:
    """
    Fetch summary metrics for a given event.
    Returns:
        total_invited: total guests for the event
        total_rsvp_yes: invitations accepted
        total_rsvp_no: invitations declined
        total_no_response: invitations pending
        total_entered: scanned attendees
        total_vip: VIP guests
        total_normal: Normal guests
    """
    try:
        # Aggregate guest counts
        guest_counts = (
            db.query(
                func.count(Guest.id).label("total_invited"),
                func.count(func.nullif(Guest.guest_type != "VIP", True)).label("total_vip"),
                func.count(func.nullif(Guest.guest_type != "NORMAL", True)).label("total_normal"),
            )
            .filter(Guest.event_id == event_id)
            .first()
        )

        # Aggregate RSVP counts
        rsvp_counts = (
            db.query(
                func.count(func.nullif(Invitation.rsvp_status != "YES", True)).label("total_rsvp_yes"),
                func.count(func.nullif(Invitation.rsvp_status != "NO", True)).label("total_rsvp_no"),
                func.count(func.nullif(Invitation.rsvp_status != "PENDING", True)).label("total_no_response"),
            )
            .filter(Invitation.event_id == event_id)
            .first()
        )

        # Attendance count
        total_entered = (
            db.query(func.count(AttendanceLog.id))
            .filter(AttendanceLog.event_id == event_id, AttendanceLog.scan_status == "ENTERED")
            .scalar()
        )

        return {
            "total_invited": guest_counts.total_invited or 0,
            "total_vip": guest_counts.total_vip or 0,
            "total_normal": guest_counts.total_normal or 0,
            "total_rsvp_yes": rsvp_counts.total_rsvp_yes or 0,
            "total_rsvp_no": rsvp_counts.total_rsvp_no or 0,
            "total_no_response": rsvp_counts.total_no_response or 0,
            "total_entered": total_entered or 0,
        }

    except Exception as e:
        # Log error in production (replace print with logging)
        print(f"[AnalyticsService] Failed to fetch event summary: {e}")
        return {
            "total_invited": 0,
            "total_vip": 0,
            "total_normal": 0,
            "total_rsvp_yes": 0,
            "total_rsvp_no": 0,
            "total_no_response": 0,
            "total_entered": 0,
        }
