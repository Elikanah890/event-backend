from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.guest import GuestCreate, GuestRead
from app.models.guest import Guest
from app.utils.csv_import import parse_guest_csv
from app.core.database import get_db
from datetime import datetime

router = APIRouter(prefix="/guests", tags=["guests"])

@router.post("/", response_model=GuestRead)
def create_guest(guest_in: GuestCreate, db: Session = Depends(get_db)):
    guest = Guest(
        event_id=guest_in.event_id,
        name=guest_in.name,
        title=guest_in.title,
        guest_type=guest_in.guest_type,
        contact=guest_in.contact,
        created_at=datetime.utcnow()
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

@router.post("/bulk/{event_id}", response_model=list[GuestRead])
def bulk_upload_guests(event_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    guest_data = parse_guest_csv(path)
    guests = []
    for g in guest_data:
        guest = Guest(
            event_id=event_id,
            name=g["name"],
            title=g.get("title"),
            guest_type=g.get("guest_type", "NORMAL"),
            contact=g.get("contact"),
            created_at=datetime.utcnow()
        )
        db.add(guest)
        guests.append(guest)
    db.commit()
    for g in guests:
        db.refresh(g)
    return guests
