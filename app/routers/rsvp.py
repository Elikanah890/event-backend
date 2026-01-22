from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.rsvp_service import update_rsvp
from app.schemas.invitation import InvitationRead
from app.core.database import get_db

router = APIRouter(prefix="/rsvp", tags=["rsvp"])

# Valid RSVP statuses
VALID_RSVP_STATUSES = {"YES", "NO", "PENDING"}

@router.post("/{invitation_token}", response_model=InvitationRead)
def rsvp_guest(
    invitation_token: str,
    rsvp_status: str = Query(..., description="RSVP status: YES, NO, or PENDING"),
    db: Session = Depends(get_db)
):
    # Normalize and validate RSVP status
    rsvp_status = rsvp_status.upper()
    if rsvp_status not in VALID_RSVP_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid RSVP status: {rsvp_status}")

    # Update RSVP in DB
    invitation = update_rsvp(db, invitation_token, rsvp_status)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    return invitation
