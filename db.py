import sqlite3

from config import DB_PATH


def init_db() -> None:
    """Create the applications table if it does not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                contact TEXT,
                service_type TEXT,
                day TEXT,
                preferred_time TEXT,
                comment TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_application(
    user_id: int,
    username: str,
    name: str,
    phone: str,
    service: str,
    day: str,
    pref_time: str,
    comment: str,
) -> None:
    """Insert a new application with pending status."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO applications(
                user_id, username, name, contact, service_type, day,
                preferred_time, comment, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, name, phone, service, day, pref_time, comment, "pending"),
        )
        conn.commit()


def get_taken_slots(service: str, day: str) -> list[str]:
    """Return a list of already taken preferred_time values for the given service/day."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT preferred_time FROM applications WHERE service_type = ? AND day = ? AND status = 'pending'",
            (service, day),
        )
        taken_rows = cursor.fetchall()

    return [row[0] for row in taken_rows]
