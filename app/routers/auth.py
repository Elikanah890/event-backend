from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.schemas.admin import (
    AdminCreate,
    AdminLogin,
    AdminRead,
    TokenResponse,
)
from app.services.auth_service import register_admin, authenticate_admin, get_current_admin
from app.core.database import get_db
from app.models.admin import Admin

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # For JWT bearer token

# -----------------------
# Existing endpoints
# -----------------------
@router.post("/register", response_model=AdminRead, status_code=status.HTTP_201_CREATED)
def admin_register(admin_in: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter_by(email=admin_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    admin = register_admin(db, admin_in)
    return admin

@router.post("/login", response_model=TokenResponse)
def admin_login(admin_in: AdminLogin, db: Session = Depends(get_db)):
    token_data = authenticate_admin(db, admin_in.email, admin_in.password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return token_data

# -----------------------
# New endpoint: /me
# -----------------------
@router.get("/me", response_model=AdminRead)
def read_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Return the currently logged-in admin based on JWT token.
    """
    admin = get_current_admin(db, token)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return admin
