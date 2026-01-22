from sqlalchemy import Column, BigInteger, String, Text, Enum, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum('ACTIVE', 'FINISHED', name='event_status'), default='ACTIVE', index=True)
    created_by = Column(BigInteger, ForeignKey("admins.id"), nullable=False)
    created_at = Column(TIMESTAMP)

    admin = relationship("Admin", backref="events")
    guests = relationship("Guest", back_populates="event", cascade="all, delete")
    invitations = relationship("Invitation", back_populates="event", cascade="all, delete")
    attendance_logs = relationship("AttendanceLog", back_populates="event", cascade="all, delete")
