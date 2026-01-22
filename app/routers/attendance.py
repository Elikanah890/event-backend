from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.attendance import AttendanceLog
from app.models.invitation import Invitation
from app.schemas.attendance import AttendanceRead
from app.core.database import get_db

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/scan/{invitation_token}", response_model=AttendanceRead)
def scan_qr(invitation_token: str, db: Session = Depends(get_db)):
    """
    Scan a guest's QR code to mark attendance.

    Checks:
      - Invitation exists
      - RSVP = YES
      - QR not already used
    """

    # Find the invitation
    invitation = db.query(Invitation).filter(
        Invitation.invitation_token == invitation_token
    ).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    # Check RSVP
    if invitation.rsvp_status != "YES":
        raise HTTPException(status_code=400, detail="Guest has not RSVPed YES")

    # Check if attendance already recorded
    existing_attendance = db.query(AttendanceLog).filter(
        AttendanceLog.guest_id == invitation.guest_id,
        AttendanceLog.event_id == invitation.event_id
    ).first()

    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance already recorded")

    # Record attendance
    attendance = AttendanceLog(
        guest_id=invitation.guest_id,
        event_id=invitation.event_id,
        invitation_id=invitation.id,
        scanned_at=datetime.utcnow(),
        scan_status="ENTERED"
    )
    db.add(attendance)

    # Mark invitation as used
    invitation.status = "USED"

    db.commit()
    db.refresh(attendance)

    return attendance
