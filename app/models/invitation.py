from sqlalchemy import Column, BigInteger, String, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(BigInteger, primary_key=True, index=True)
    event_id = Column(BigInteger, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    guest_id = Column(BigInteger, ForeignKey("guests.id", ondelete="CASCADE"), nullable=False)
    
    # Generate a UUID string automatically if not provided
    invitation_token = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    
    qr_hash = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: uuid.uuid4().hex  # Simple QR hash placeholder
    )
    
    rsvp_status = Column(
        Enum('YES', 'NO', 'PENDING', name='rsvp_status_enum'),
        default='PENDING',
        index=True
    )
    
    sent_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    event = relationship("Event", back_populates="invitations")
    guest = relationship("Guest", back_populates="invitations")
    attendance_log = relationship(
        "AttendanceLog",
        back_populates="invitation",
        uselist=False,
        cascade="all, delete"
    )
