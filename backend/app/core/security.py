"""Security utilities for JWT, password hashing, and authentication."""

from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.app.core.config import get_settings

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Token payload data."""

    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[datetime] = None


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.jwt_expiration
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        seconds=settings.jwt_refresh_expiration
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        token_data = TokenData(user_id=user_id)
        return token_data
    except JWTError:
        return None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength based on requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if settings.password_require_uppercase and not any(
        c.isupper() for c in password
    ):
        return False, "Password must contain at least one uppercase letter"

    if settings.password_require_numbers and not any(
        c.isdigit() for c in password
    ):
        return False, "Password must contain at least one number"

    if settings.password_require_special and not any(
        c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password
    ):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"
