"""Security helpers, JWT service and password hashing utilities."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import bcrypt
import jwt

from src.shared.config import get_jwt_secret, get_settings


def get_cors_settings() -> dict:
    """Return strict CORS defaults; override via settings in bootstrap."""
    return {
        "allow_origins": [],
        "allow_credentials": False,
        "allow_methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type"],
    }


# =========================
# Password hashing (bcrypt)
# =========================

def hash_password(password: str, *, rounds: int = 12) -> str:
    if not isinstance(password, str) or password == "":
        raise ValueError("Password must be a non-empty string")
    salt = bcrypt.gensalt(rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    if not password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


# ============
# JWT service
# ============

def create_token(
    data: Dict[str, Any],
    *,
    expires_minutes: Optional[int] = None,
    secret: Optional[str] = None,
) -> str:
    """Create a signed JWT including iat/exp claims.

    - `data` should be small, non-sensitive claims (e.g., {"sub": user_id}).
    - `expires_minutes` defaults to configured ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    settings = get_settings()
    algorithm = getattr(settings, "JWT_ALGORITHM", "HS256")
    expire_in = expires_minutes if expires_minutes is not None else getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    now = datetime.now(timezone.utc)
    payload = {**data, "iat": int(now.timestamp())}
    if expire_in and expire_in > 0:
        payload["exp"] = int((now + timedelta(minutes=expire_in)).timestamp())

    secret_key = secret or get_jwt_secret()
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    # PyJWT returns str for modern versions
    return token


def verify_token(token: str, *, secret: Optional[str] = None) -> Dict[str, Any]:
    """Verify and decode a JWT, raising ValueError on failure."""
    if not token:
        raise ValueError("Token is required")

    settings = get_settings()
    algorithm = getattr(settings, "JWT_ALGORITHM", "HS256")
    secret_key = secret or get_jwt_secret()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc


