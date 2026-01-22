from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None  # ACTIVE / FINISHED

class EventRead(EventBase):
    id: int
    status: str
    created_by: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True  # updated for Pydantic v2
