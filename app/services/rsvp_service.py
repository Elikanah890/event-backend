from sqlalchemy.orm import Session
from app.models.invitation import Invitation
from datetime import datetime

# Allowed RSVP statuses
VALID_RSVP_STATUSES = {"YES", "NO", "PENDING"}

def update_rsvp(db: Session, invitation_token: str, rsvp_status: str) -> Invitation | None:
    """
    Update the RSVP status for an invitation identified by its token.

    Args:
        db (Session): SQLAlchemy database session.
        invitation_token (str): UUID token for the invitation.
        rsvp_status (str): New RSVP status ('YES', 'NO', 'PENDING').

    Returns:
        Invitation | None: Updated Invitation object or None if not found.
    """
    # Normalize RSVP status
    rsvp_status = rsvp_status.upper()
    if rsvp_status not in VALID_RSVP_STATUSES:
        raise ValueError(f"Invalid RSVP status: {rsvp_status}. Must be one of {VALID_RSVP_STATUSES}")

    # Find the invitation
    invitation = db.query(Invitation).filter(
        Invitation.invitation_token == invitation_token
    ).first()

    if not invitation:
        return None

    # Update RSVP and commit
    invitation.rsvp_status = rsvp_status
    invitation.updated_at = datetime.utcnow()  # optional, if you track updates
    db.commit()
    db.refresh(invitation)
    return invitation
