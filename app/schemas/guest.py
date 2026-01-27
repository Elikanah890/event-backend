from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import datetime


class GuestBase(BaseModel):
    full_name: str
    title: Optional[str] = None
    guest_type: str = "NORMAL"
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    profile_photo_url: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = True

    # Validate guest_type
    @field_validator("guest_type")
    @classmethod
    def validate_guest_type(cls, v):
        if v not in {"VIP", "NORMAL"}:
            raise ValueError("guest_type must be VIP or NORMAL")
        return v


class GuestCreate(GuestBase):
    event_id: int

    # Validate at least one contact (email or phone) only on creation
    @model_validator(mode="before")
    @classmethod
    def validate_contact(cls, values):
        email, phone = values.get("email"), values.get("phone")
        if not email and not phone:
            raise ValueError("At least one of email or phone is required")
        return values


class GuestUpdate(BaseModel):
    full_name: Optional[str]
    title: Optional[str]
    guest_type: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    organization: Optional[str]
    profile_photo_url: Optional[str]
    notes: Optional[str]
    is_active: Optional[bool]

    # Validate guest_type if provided
    @field_validator("guest_type")
    @classmethod
    def validate_guest_type(cls, v):
        if v and v not in {"VIP", "NORMAL"}:
            raise ValueError("guest_type must be VIP or NORMAL")
        return v

    # Validate at least one contact (email or phone) only on update
    @model_validator(mode="before")
    @classmethod
    def validate_contact(cls, values):
        email, phone = values.get("email"), values.get("phone")
        if email is None and (phone is None or phone.strip() == ""):
            raise ValueError("At least one of email or phone is required")
        return values


class GuestRead(GuestBase):
    id: int
    event_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Pydantic V2 replacement for orm_mode
