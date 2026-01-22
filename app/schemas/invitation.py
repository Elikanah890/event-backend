from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvitationBase(BaseModel):
    event_id: int
    guest_id: int
    rsvp_status: Optional[str] = "PENDING"  # YES / NO / PENDING

class InvitationCreate(InvitationBase):
    pass

class InvitationRead(InvitationBase):
    id: int
    invitation_token: str
    qr_hash: str
    sent_at: Optional[datetime]       # Use datetime instead of str
    created_at: Optional[datetime]    # Use datetime instead of str

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }
