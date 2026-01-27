from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.core.database import get_db
from app.schemas.guest import GuestCreate, GuestRead
from app.models.guest import Guest
from app.models.event import Event
from app.utils.csv_import import parse_guest_csv

router = APIRouter(prefix="/guests", tags=["guests"])


def validate_event(db: Session, event_id: int) -> Event:
    """Ensure the event exists."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id={event_id} not found")
    return event


@router.post("/", response_model=GuestRead, status_code=status.HTTP_201_CREATED)
def create_guest(guest_in: GuestCreate, db: Session = Depends(get_db)):
    validate_event(db, guest_in.event_id)

    guest = Guest(
        event_id=guest_in.event_id,
        full_name=guest_in.full_name,
        title=guest_in.title,
        guest_type=(guest_in.guest_type or "NORMAL").upper(),
        email=guest_in.email or None,
        phone=guest_in.phone or None,
        organization=guest_in.organization,
        profile_photo_url=guest_in.profile_photo_url,
        notes=guest_in.notes,
        is_active=guest_in.is_active if hasattr(guest_in, "is_active") else True,
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


@router.get("/{guest_id}", response_model=GuestRead)
def get_guest_profile(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.id == guest_id, Guest.is_active == True).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.email = guest.email or None
    guest.phone = guest.phone or None
    return guest


@router.post("/bulk/{event_id}", response_model=List[GuestRead], status_code=status.HTTP_201_CREATED)
def bulk_upload_guests(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    event = validate_event(db, event_id)

    tmp_path = Path("/tmp") / file.filename

    try:
        with open(tmp_path, "wb") as f:
            f.write(file.file.read())

        guest_data = parse_guest_csv(tmp_path)
        if not guest_data:
            raise HTTPException(status_code=400, detail="CSV file is empty or invalid")

        guests: List[Guest] = []

        for row in guest_data:
            # Skip invalid rows (must have full_name or at least email/phone)
            if not row.get("full_name") and not (row.get("email") or row.get("phone")):
                continue

            guest = Guest(
                event_id=event.id,
                full_name=row.get("full_name") or "",
                title=row.get("title"),
                guest_type=(row.get("guest_type") or "NORMAL").upper(),
                email=row.get("email") or None,
                phone=row.get("phone") or None,
                organization=row.get("organization"),
                profile_photo_url=row.get("profile_photo_url"),
                notes=row.get("notes"),
                is_active=row.get("is_active", True),
            )
            db.add(guest)
            guests.append(guest)

        if not guests:
            raise HTTPException(status_code=400, detail="No valid guest rows found in CSV")

        db.commit()
        for g in guests:
            db.refresh(g)

        return guests

    finally:
        # Delete temp file safely
        tmp_path.unlink(missing_ok=True)


# ------------------- NEW GET ROUTE -------------------
@router.get("/", response_model=List[GuestRead])
def get_guests_by_event(event_id: int, db: Session = Depends(get_db)):
    """
    Fetch all guests for a specific event.
    Example: GET /guests/?event_id=8
    """
    validate_event(db, event_id)
    guests = db.query(Guest).filter(Guest.event_id == event_id, Guest.is_active == True).all()
    return guests
# ------------------- DELETE GUEST -------------------
@router.delete("/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    """
    Soft-delete a guest by setting is_active=False.
    """
    guest = db.query(Guest).filter(Guest.id == guest_id, Guest.is_active == True).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    guest.is_active = False
    db.commit()
    return
