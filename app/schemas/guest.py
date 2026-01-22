from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GuestBase(BaseModel):
    name: str
    title: Optional[str] = None
    guest_type: Optional[str] = "NORMAL"  # VIP / NORMAL
    contact: Optional[str]

class GuestCreate(GuestBase):
    event_id: int

class GuestUpdate(BaseModel):
    name: Optional[str]
    title: Optional[str]
    guest_type: Optional[str]
    contact: Optional[str]

class GuestRead(GuestBase):
    id: int
    event_id: int
    created_at: Optional[datetime]  # Keep as datetime for proper serialization

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode
