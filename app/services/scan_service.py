from sqlalchemy.orm import Session
from app.models.attendance import AttendanceLog
from app.models.invitation import Invitation
from datetime import datetime

def scan_qr(db: Session, invitation_token: str):
    invitation = db.query(Invitation).filter(Invitation.invitation_token == invitation_token).first()
    if not invitation:
        return {"status": "REJECTED", "reason": "Invalid invitation"}

    if invitation.rsvp_status != "YES":
        return {"status": "REJECTED", "reason": "RSVP not confirmed"}

    # Check if already scanned
    existing_log = db.query(AttendanceLog).filter(AttendanceLog.invitation_id == invitation.id).first()
    if existing_log:
        return {"status": "REJECTED", "reason": "Already scanned"}

    attendance = AttendanceLog(
        event_id=invitation.event_id,
        guest_id=invitation.guest_id,
        invitation_id=invitation.id,
        scanned_at=datetime.utcnow(),
        scan_status="ENTERED"
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return {"status": "ENTERED", "scanned_at": attendance.scanned_at}
