from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.schemas.invitation import InvitationRead
from app.models.invitation import Invitation
from app.models.guest import Guest
from app.models.event import Event
from app.core.database import get_db

router = APIRouter(prefix="/invitations", tags=["invitations"])

@router.post("/{guest_id}", response_model=InvitationRead)
def create_invitation(
    guest_id: int,
    event_id: int,
    db: Session = Depends(get_db)
):
    # Ensure guest exists
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    # Ensure event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Prevent duplicate invitation
    existing = (
        db.query(Invitation)
        .filter(
            Invitation.guest_id == guest_id,
            Invitation.event_id == event_id
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Invitation already exists for this guest and event"
        )

    invitation = Invitation(
        guest_id=guest_id,
        event_id=event_id,
        invitation_token=str(uuid.uuid4()),
        qr_hash=uuid.uuid4().hex,
        rsvp_status="PENDING",
        created_at=datetime.utcnow()
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation
