"""Domain entities for the users context."""

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    email: str
    password_hash: str
    name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(*, email: str, password_hash: str, name: Optional[str] = None) -> "User":
        normalized = (email or "").strip().lower()
        if not normalized or "@" not in normalized:
            raise ValueError("Invalid email")
        if not password_hash:
            raise ValueError("password_hash is required")
        return User(id=None, email=normalized, password_hash=password_hash, name=name, is_active=True)

    def with_updates(self, *, name: Optional[str] = None, is_active: Optional[bool] = None, password_hash: Optional[str] = None) -> "User":
        return replace(
            self,
            name=self.name if name is None else name,
            is_active=self.is_active if is_active is None else is_active,
            password_hash=self.password_hash if password_hash is None else password_hash,
        )





