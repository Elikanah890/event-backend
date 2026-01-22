from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.attendance import AttendanceLog
from app.models.invitation import Invitation
from app.models.guest import Guest

def get_event_summary(db: Session, event_id: int):
    total_invited = db.query(Guest).filter(Guest.event_id == event_id).count()
    total_rsvp_yes = db.query(Invitation).filter(Invitation.event_id == event_id, Invitation.rsvp_status == "YES").count()
    total_rsvp_no = db.query(Invitation).filter(Invitation.event_id == event_id, Invitation.rsvp_status == "NO").count()
    total_no_response = db.query(Invitation).filter(Invitation.event_id == event_id, Invitation.rsvp_status == "PENDING").count()
    total_entered = db.query(AttendanceLog).filter(AttendanceLog.event_id == event_id, AttendanceLog.scan_status == "ENTERED").count()
    total_vip = db.query(Guest).filter(Guest.event_id == event_id, Guest.guest_type == "VIP").count()
    total_normal = db.query(Guest).filter(Guest.event_id == event_id, Guest.guest_type == "NORMAL").count()

    return {
        "total_invited": total_invited,
        "total_rsvp_yes": total_rsvp_yes,
        "total_rsvp_no": total_rsvp_no,
        "total_no_response": total_no_response,
        "total_entered": total_entered,
        "total_vip": total_vip,
        "total_normal": total_normal
    }
