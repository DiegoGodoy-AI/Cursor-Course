"""Ports (interfaces) for the users context."""

from typing import Protocol, Optional

from ..domain.entities import User


class UserRepository(Protocol):
    def create_user(self, user: User) -> int:
        ...

    def get_user_by_email(self, email: str) -> Optional[User]:
        ...

    def update_user(self, user: User) -> None:
        ...





