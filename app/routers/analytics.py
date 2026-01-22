from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.analytics_service import get_event_summary
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/{event_id}", summary="Get analytics for a specific event")
def analytics(event_id: int, db: Session = Depends(get_db)):
    """
    Returns a summary of event analytics including:
    total guests, RSVPs, attendance, and guest types (VIP/Normal)
    """
    try:
        summary = get_event_summary(db, event_id)
        if not summary["total_invited"]:
            # Optionally, return 404 if no event exists
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analytics found for event_id {event_id}"
            )
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch analytics: {e}"
        )
