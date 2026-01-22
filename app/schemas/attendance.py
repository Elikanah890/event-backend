from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceBase(BaseModel):
    scan_status: str  # ENTERED / REJECTED
    reason: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    event_id: int
    guest_id: int
    invitation_id: int

class AttendanceRead(AttendanceBase):
    id: int
    event_id: int
    guest_id: int
    invitation_id: int
    scanned_at: Optional[datetime]

    class Config:
        from_attributes = True  # Updated for Pydantic v2
