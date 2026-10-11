"""Account authentication ug password security."""
import hashlib
import hmac
import os
import sqlite3
from database import connect
from validators import validate_registration

ITERATIONS = 310_000


def _hash(password, salt=None):
    # Hatagan og random salt ang password, then himoon og PBKDF2 hash.
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def _verify(password, encoded):
    # I-hash ang gi-type nga password, then safe nga i-compare sa saved hash.
    try:
        method, rounds, salt, expected = encoded.split("$")
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(rounds)).hex()
        return method == "pbkdf2_sha256" and hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def admin_exists(path=None):
    # Check kung naa nay Admin para mahibaw-an kung Setup o Login ang ipakita.
    with connect(path) as db:
        return db.execute("SELECT 1 FROM users WHERE role='Admin' LIMIT 1").fetchone() is not None


def register(full_name, username, password, confirm, email, role="User", path=None):
    # I-check sa ang form fields before i-save ang account.
    validate_registration(full_name, username, password, confirm, email)
    with connect(path) as db:
        if role == "Admin":
            # First Admin ra ang mahimo sa initial setup.
            if db.execute("SELECT 1 FROM users WHERE role='Admin'").fetchone():
                raise ValueError("Initial Admin setup is already complete.")
        else:
            # Public registration = User ra; dili pwede mag-sign up as Admin.
            role = "User"
        try:
            # Password hash ra ang i-save sa database, dili ang actual password.
            db.execute("INSERT INTO users(full_name,username,password_hash,email,role) VALUES(?,?,?,?,?)",
                       (full_name.strip(), username.strip(), _hash(password), email.strip(), role))
        except sqlite3.IntegrityError as exc:
            raise ValueError("Username already exists.") from exc


def login(username, password, path=None):
    # Pangitaa ang username; successful login ra kung sakto ang password.
    with connect(path) as db:
        user = db.execute("SELECT id,full_name,username,password_hash,email,role FROM users WHERE username=?", (username.strip(),)).fetchone()
    if not user or not _verify(password, user["password_hash"]):
        raise ValueError("Incorrect username or password.")
    return dict(user)
