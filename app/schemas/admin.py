from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Used for creating admin
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Used for reading admin info (safe)
class AdminRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# Used for login request
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# Used for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
