from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from app.core.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
