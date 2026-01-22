import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing using bcrypt directly
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt. Truncate to 72 bytes to avoid bcrypt limit.
    Returns the hashed password as a UTF-8 string.
    """
    password_bytes = password.encode("utf-8")[:72]  # bcrypt max length
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Truncates password to 72 bytes.
    """
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# JWT token generation
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with optional expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """
    Decode a JWT token. Returns payload dict if valid, else None.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
