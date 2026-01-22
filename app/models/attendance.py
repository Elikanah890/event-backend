from sqlalchemy import Column, BigInteger, String, Enum, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    __table_args__ = (
        UniqueConstraint('invitation_id', name='uq_single_entry'),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    event_id = Column(BigInteger, ForeignKey("events.id"), nullable=False)
    guest_id = Column(BigInteger, ForeignKey("guests.id"), nullable=False)
    invitation_id = Column(BigInteger, ForeignKey("invitations.id"), nullable=False)
    scanned_at = Column(TIMESTAMP)
    scan_status = Column(Enum('ENTERED', 'REJECTED', name='scan_status_enum'), nullable=False)
    reason = Column(String(255), nullable=True)

    event = relationship("Event", back_populates="attendance_logs")
    guest = relationship("Guest", back_populates="attendance_logs")
    invitation = relationship("Invitation", back_populates="attendance_log")
