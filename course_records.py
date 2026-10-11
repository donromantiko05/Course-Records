"""Course record actions: add, view, edit, delete, search, ug filter."""
import sqlite3
from database import connect
from validators import validate_course

FIELDS = ("course_id", "course_code", "course_name", "department", "academic_program", "units", "semester", "school_year", "instructor_name", "status")


def list_courses(search="", filters=None, path=None):
    # Safe query ni; ang search ug filter inputs dili diretso idugtong sa SQL.
    filters = filters or {}
    sql = "SELECT * FROM courses WHERE 1=1"
    args = []
    if search.strip():
        sql += " AND (course_id LIKE ? COLLATE NOCASE OR course_code LIKE ? COLLATE NOCASE OR course_name LIKE ? COLLATE NOCASE OR instructor_name LIKE ? COLLATE NOCASE OR department LIKE ? COLLATE NOCASE OR academic_program LIKE ? COLLATE NOCASE)"
        args.extend([f"%{search.strip()}%"] * 6)
    for key in ("department", "academic_program", "semester", "status"):
        if filters.get(key):
            sql += f" AND {key}=?"
            args.append(filters[key])
    sql += " ORDER BY course_code COLLATE NOCASE"
    with connect(path) as db:
        return [dict(row) for row in db.execute(sql, args)]


def save_course(data, record_id=None, path=None):
    # Walay record_id = add new course; naa = update existing course.
    units = validate_course(data)
    values = [data[k].strip() for k in FIELDS]
    values[5] = units
    with connect(path) as db:
        try:
            if record_id is None:
                db.execute(f"INSERT INTO courses({','.join(FIELDS)}) VALUES({','.join('?' for _ in FIELDS)})", values)
            else:
                assignments = ",".join(f"{field}=?" for field in FIELDS)
                db.execute(f"UPDATE courses SET {assignments}, updated_at=CURRENT_TIMESTAMP WHERE id=?", values + [record_id])
                if db.total_changes == 0:
                    raise ValueError("The selected course no longer exists.")
        except sqlite3.IntegrityError as exc:
            # Klarohon ang error kung duplicate ang Course ID o Course Code.
            message = str(exc).lower()
            if "course_id" in message:
                raise ValueError("Course ID already exists.") from exc
            if "course_code" in message:
                raise ValueError("Course Code already exists.") from exc
            raise ValueError("Could not save this course. Check the entered values.") from exc


def delete_course(record_id, path=None):
    # Delete ang course gamit ang internal database ID.
    with connect(path) as db:
        cur = db.execute("DELETE FROM courses WHERE id=?", (record_id,))
        if cur.rowcount == 0:
            raise ValueError("The selected course no longer exists.")


def statistics(path=None):
    # Count ang tanan courses, apil ang Active ug Inactive.
    with connect(path) as db:
        row = db.execute("SELECT COUNT(*) total, SUM(status='Active') active, SUM(status='Inactive') inactive FROM courses").fetchone()
        return {k: row[k] or 0 for k in ("total", "active", "inactive")}


def filter_values(path=None):
    # Get ang unique departments ug programs para sa filter dropdowns.
    with connect(path) as db:
        return {key: [r[0] for r in db.execute(f"SELECT DISTINCT {key} FROM courses ORDER BY {key}")] for key in ("department", "academic_program")}
