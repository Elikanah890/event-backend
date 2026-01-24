from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventUpdate, EventRead
from app.models.event import Event
from app.core.database import get_db
from datetime import datetime
from typing import List

router = APIRouter(prefix="/events", tags=["events"])

# ----------------------------
# Simulated current admin logic
# ----------------------------
# Replace with actual auth logic (JWT/session) in production
def get_current_admin_id() -> int:
    return 1  # hardcoded for now; replace with auth

# ----------------------------
# Create Event
# ----------------------------
@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate, db: Session = Depends(get_db)):
    admin_id = get_current_admin_id()

    db_event = Event(
        name=event_in.name,
        location=event_in.location,
        description=event_in.description,
        start_time=event_in.start_time,
        end_time=event_in.end_time,
        status="ACTIVE",
        created_by=admin_id,
        created_at=datetime.utcnow()
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# ----------------------------
# Get single Event
# ----------------------------
@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# ----------------------------
# List all Events (optional)
# ----------------------------
@router.get("/", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

# ----------------------------
# Update Event
# ----------------------------
@router.put("/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_in: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = event_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

# ----------------------------
# Delete Event
# ----------------------------
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"detail": "Event deleted"}
