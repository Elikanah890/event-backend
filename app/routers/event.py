from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventUpdate, EventRead
from app.models.event import Event
from app.core.database import get_db
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventRead)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), admin_id: int = 1):
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

@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_in: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Only update fields provided in request
    update_data = event_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"detail": "Event deleted"}
