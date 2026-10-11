# Course Records Management System

A local Python desktop application for managing course catalog records. It covers course data only; it does not handle enrollment, grades, attendance, or billing. Demo data is not inserted automatically.

## Features

- CustomTkinter desktop screens for one-time Admin setup, login, registration, and dashboard.
- SQLite persistence for users and all ten course fields: Course ID, Course Code, Course Name, Department, Academic Program, Units, Semester, School Year, Instructor Name, and Status.
- Admin add, edit, and delete controls; User accounts are read-only. Both roles can search and combine filters.
- Partial case-insensitive search across ID, code, name, instructor, department, and program; department, program, semester, and status filters.
- Course totals and Active/Inactive counts, validation, confirmation prompts, and PBKDF2-HMAC password hashes with random salts.

## Setup and run

Requires Python 3.10+ and a desktop session. From this folder, run:

```powershell
python -m pip install -r requirements.txt
python main.py
```

CustomTkinter was present in the implementation environment. Tkinter and SQLite are part of the Python installation. The database is created automatically at `data/course_records.db` and retained across launches.

## First Admin and accounts

On a new database, the first screen is Initial Admin Setup. Complete the form with a full name, username, password, confirmation, and email. Username policy: at least four characters, using letters, numbers, dot, underscore, or hyphen. Passwords need seven or more characters, with uppercase, lowercase, and a number. After an Admin exists, the setup screen disappears and public registration always creates User accounts. Registration checks all fields, email format, and duplicate usernames. Log out to clear the in-memory session and return to login.

## Roles

Admin can read, add, update, and delete course records. User can read, search, and filter only. The GUI checks the session role before opening course write actions; the account role is loaded from SQLite after credential verification.

## Demonstrating to an instructor

1. Launch the app and create the first Admin.
2. Add a course with all ten fields; select it and update it, then demonstrate a confirmed delete.
3. Add another course and search a partial course code or name; combine Department, Program, Semester, and Status filters, then press Reset.
4. Log out, register a User, log in, and show that the records remain searchable while write controls are absent.
5. Close and reopen the app to show persisted accounts and courses.
6. Run the business logic tests with `python -m unittest discover -s tests -v`.

## How the code is organized

- `main.py` starts the application.
- `database.py` owns the schema, SQLite connection, and initialization.
- `auth.py` hashes passwords, registers accounts, and verifies logins.
- `validators.py` contains reusable account and course validation.
- `course_records.py` contains parameterized course CRUD, search, filters, and statistics.
- `ui.py` contains screens, forms, role checks, and feedback dialogs.
- `tests/test_core.py` uses a separate temporary database for business logic checks.

## Limitations

There is no Admin account management screen, import/export, or bundled sample data. GUI automation is not included. The setup route is available whenever the database has no Admin account, including if all Admin accounts are manually removed from the database.
