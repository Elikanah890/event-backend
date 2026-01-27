from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Guest(Base):
    __tablename__ = "guests"

    id = Column(BigInteger, primary_key=True, index=True)

    # Relations
    event_id = Column(
        BigInteger,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Identity
    full_name = Column(String(150), nullable=False)
    title = Column(String(100), nullable=True)
    guest_type = Column(
        Enum("VIP", "NORMAL", name="guest_type_enum"),
        nullable=False,
        default="NORMAL",
        index=True,
    )

    # Contact
    email = Column(String(150), nullable=True, index=True)
    phone = Column(String(50), nullable=True, index=True)

    # Profile
    profile_photo_url = Column(String(255), nullable=True)
    organization = Column(String(150), nullable=True)
    notes = Column(Text, nullable=True)

    # System
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    event = relationship("Event", back_populates="guests")
    invitations = relationship(
        "Invitation", back_populates="guest", cascade="all, delete"
    )
    attendance_logs = relationship(
        "AttendanceLog", back_populates="guest", cascade="all, delete"
    )
