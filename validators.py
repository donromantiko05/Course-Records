"""Reusable checks para sa account ug course info."""
import re

SEMESTERS = ("1st Semester", "2nd Semester", "Summer")
STATUSES = ("Active", "Inactive")


def valid_email(value):
    # Quick check kung sakto ba tan-awon ang email format.
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value.strip()))


def validate_registration(full_name, username, password, confirm, email):
    # Dili pwede blank ang fields; username kinahanglan allowed characters ra.
    if not all(v.strip() for v in (full_name, username, password, confirm, email)):
        raise ValueError("Please complete all required fields.")
    if len(username) < 4 or not re.fullmatch(r"[A-Za-z0-9_.-]+", username):
        raise ValueError("Username must be at least 4 characters and use only letters, numbers, dots, underscores, or hyphens.")
    # Check ang password rules ug kung match ba ang password ug confirmation.
    if len(password) < 7 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password):
        raise ValueError("Password must contain at least 7 characters, including uppercase, lowercase, and a number.")
    if password != confirm:
        raise ValueError("Passwords do not match.")
    if not valid_email(email):
        raise ValueError("Please enter a valid email address.")


def validate_course(data):
    # Tan-awa kung kompleto ang required course fields before save.
    required = ("course_id", "course_code", "course_name", "department", "academic_program", "semester", "school_year", "instructor_name", "status")
    if any(not str(data.get(k, "")).strip() for k in required):
        raise ValueError("Please complete all required course fields.")
    # Units kinahanglan number nga greater than zero.
    try:
        units = float(data["units"])
    except (TypeError, ValueError):
        raise ValueError("Units must be a number greater than zero.") from None
    if units <= 0:
        raise ValueError("Units must be a number greater than zero.")
    # Siguroha nga valid ang semester, status, ug school year format.
    if data["semester"] not in SEMESTERS:
        raise ValueError("Choose an allowed semester.")
    if data["status"] not in STATUSES:
        raise ValueError("Status must be Active or Inactive.")
    year = data["school_year"].strip()
    if not re.fullmatch(r"\d{4}-\d{4}", year) or int(year[5:]) != int(year[:4]) + 1:
        raise ValueError("School Year must use YYYY-YYYY format (for example, 2026-2027).")
    return units
