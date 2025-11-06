"""SQLite implementation of UserRepository using shared connection utilities."""

from typing import Optional

from sqlite3 import Connection

from src.shared.database import get_connection
from ...application.ports import UserRepository
from ...domain.entities import User


def _ensure_schema(conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            name TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    conn.commit()


def _row_to_domain(row: tuple) -> User:
    return User(
        id=row[0],
        email=row[1],
        password_hash=row[2],
        name=row[3],
        is_active=bool(row[4]),
        created_at=row[5],
        updated_at=row[6],
    )


class SQLiteUserRepository(UserRepository):
    def __init__(self) -> None:
        # Ensure table exists on first use
        conn = get_connection()
        try:
            _ensure_schema(conn)
        finally:
            conn.close()

    def create_user(self, user: User) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO users (email, password_hash, name, is_active)
                VALUES (?, ?, ?, ?)
                """,
                (user.email.lower(), user.password_hash, user.name, 1 if user.is_active else 0),
            )
            user_id = cur.lastrowid
            conn.commit()
            return int(user_id)
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[User]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, email, password_hash, name, is_active, created_at, updated_at
                FROM users WHERE email = ?
                """,
                (email.lower(),),
            )
            row = cur.fetchone()
            return None if row is None else _row_to_domain(row)
        finally:
            conn.close()

    def update_user(self, user: User) -> None:
        if user.id is None:
            raise ValueError("User id is required for update")
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE users
                SET email = ?, password_hash = ?, name = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (user.email.lower(), user.password_hash, user.name, 1 if user.is_active else 0, user.id),
            )
            conn.commit()
        finally:
            conn.close()





