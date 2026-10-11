"""SQLite database setup para sa accounts ug course records."""
from pathlib import Path
import sqlite3
from contextlib import contextmanager

DATA_DIR = Path(__file__).resolve().parent / "data"
# Dinhi i-save sa app ang database file.
DB_PATH = DATA_DIR / "course_records.db"


@contextmanager
def connect(path=DB_PATH):
    # Create ang data folder kung wala pa, then connect sa database.
    path = path or DB_PATH
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        # If okay ang operation, commit; if naay error, rollback ang changes.
        with db:
            yield db
    finally:
        db.close()


def initialize(path=DB_PATH):
    # Create ang users ug courses tables kung first run pa ni.
    with connect(path) as db:
        db.executescript("""
        -- Account details ug role diri; password hash ra ang gi-store, dili plain password.
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, username TEXT NOT NULL UNIQUE,
          password_hash TEXT NOT NULL, email TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('Admin','User')),
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        -- Course info diri; dapat unique ang Course ID ug Course Code.
        CREATE TABLE IF NOT EXISTS courses (
          id INTEGER PRIMARY KEY, course_id TEXT NOT NULL UNIQUE, course_code TEXT NOT NULL UNIQUE,
          course_name TEXT NOT NULL, department TEXT NOT NULL, academic_program TEXT NOT NULL,
          units REAL NOT NULL CHECK(units > 0), semester TEXT NOT NULL,
          school_year TEXT NOT NULL, instructor_name TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('Active','Inactive')),
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)
