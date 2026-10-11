import os
import tempfile
import unittest

import auth
import course_records as cr
from database import initialize, connect
from validators import validate_registration


class CoreTests(unittest.TestCase):
    def setUp(self):
        # Fresh temporary database kada test para dili maapil ang real app data.
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        initialize(self.path)

    def tearDown(self):
        # Clean up ang temporary database human sa test.
        os.unlink(self.path)

    def test_auth_registration_login_roles_and_validation(self):
        # Test ang Admin setup, User signup, login, ug invalid account details.
        auth.register("First Admin", "admin1", "StrongPass1", "StrongPass1", "a@example.com", "Admin", self.path)
        self.assertEqual(auth.login("admin1", "StrongPass1", self.path)["role"], "Admin")
        with self.assertRaises(ValueError): auth.login("admin1", "WrongPass1", self.path)
        with self.assertRaises(ValueError): auth.register("Other", "admin1", "StrongPass1", "StrongPass1", "b@example.com", "User", self.path)
        with self.assertRaises(ValueError): auth.register("Standard User", "user01", "StrongPass1", "StrongPass1", "u@example.com", "Admin", self.path)
        auth.register("Standard User", "user01", "StrongPass1", "StrongPass1", "u@example.com", "User", self.path)
        self.assertEqual(auth.login("user01", "StrongPass1", self.path)["role"], "User")
        for vals in (("Name","user2","short","short","x@y.com"), ("Name","user3","StrongPass1","OtherPass2","x@y.com"), ("Name","user4","StrongPass1","StrongPass1","bad")):
            with self.assertRaises(ValueError): validate_registration(*vals)

    def course(self, **changes):
        data = dict(course_id="C-001", course_code="BSCS101", course_name="Intro Programming", department="Computing", academic_program="BSCS", units="3", semester="1st Semester", school_year="2026-2027", instructor_name="Alex Teacher", status="Active")
        data.update(changes)
        return data

    def test_crud_search_filter_persistence(self):
        # Test ang course validation, CRUD, search/filter, ug saved data.
        cr.save_course(self.course(), path=self.path)
        with self.assertRaisesRegex(ValueError, "Course ID"):
            cr.save_course(self.course(course_code="BSCS102"), path=self.path)
        with self.assertRaisesRegex(ValueError, "Course Code"):
            cr.save_course(self.course(course_id="C-002"), path=self.path)
        with self.assertRaises(ValueError): cr.save_course(self.course(units="letters"), path=self.path)
        with self.assertRaises(ValueError): cr.save_course(self.course(course_name=" "), path=self.path)
        self.assertEqual(len(cr.list_courses(search="program", path=self.path)), 1)
        self.assertEqual(len(cr.list_courses(search="101", filters={"department":"Computing","status":"Active"}, path=self.path)), 1)
        record = cr.list_courses(path=self.path)[0]
        cr.save_course(self.course(course_name="Updated Programming"), record["id"], self.path)
        self.assertEqual(cr.list_courses(path=self.path)[0]["course_name"], "Updated Programming")
        with connect(self.path) as db: db.execute("SELECT 1")
        self.assertEqual(cr.list_courses(path=self.path)[0]["course_code"], "BSCS101")
        cr.delete_course(record["id"], self.path)
        self.assertEqual(cr.list_courses(path=self.path), [])


if __name__ == "__main__": unittest.main()
