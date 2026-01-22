from sqlalchemy import Column, BigInteger, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Guest(Base):
    __tablename__ = "guests"

    id = Column(BigInteger, primary_key=True, index=True)
    event_id = Column(BigInteger, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    title = Column(String(100))
    guest_type = Column(Enum('VIP', 'NORMAL', name='guest_type_enum'), default='NORMAL', index=True)
    contact = Column(String(150))
    created_at = Column(TIMESTAMP)

    event = relationship("Event", back_populates="guests")
    invitations = relationship("Invitation", back_populates="guest", cascade="all, delete")
    attendance_logs = relationship("AttendanceLog", back_populates="guest", cascade="all, delete")
