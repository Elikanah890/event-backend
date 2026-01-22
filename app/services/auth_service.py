# app/services/auth_service.py

from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import JWT_SECRET_KEY
from datetime import datetime
import jwt  # Make sure PyJWT is installed

# --------------------------
# Existing functions
# --------------------------
def register_admin(db: Session, admin_in: AdminCreate) -> Admin:
    existing_admin = db.query(Admin).filter(Admin.email == admin_in.email).first()
    if existing_admin:
        return None
    hashed_pw = hash_password(admin_in.password)
    db_admin = Admin(
        name=admin_in.name,
        email=admin_in.email,
        password_hash=hashed_pw,
        created_at=datetime.utcnow()
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin or not verify_password(password, admin.password_hash):
        return None
    token = create_access_token({"sub": str(admin.id)})
    return {"access_token": token, "token_type": "bearer"}

# --------------------------
# New function for /me
# --------------------------
def get_current_admin(db: Session, token: str) -> Admin | None:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        admin_id = int(payload.get("sub"))
        if not admin_id:
            return None
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        return admin
    except Exception:
        return None
