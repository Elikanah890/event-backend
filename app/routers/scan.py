from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.scan_service import scan_qr
from app.core.database import get_db

router = APIRouter(prefix="/scan", tags=["scan"])

@router.post("/{invitation_token}")
def scan_invitation(invitation_token: str, db: Session = Depends(get_db)):
    result = scan_qr(db, invitation_token)
    return result
