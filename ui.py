"""Screens ug controls sa Course Records desktop app."""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import auth
import course_records as courses
from database import initialize
from validators import SEMESTERS, STATUSES

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CourseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Setup ang database ug main app window on startup.
        initialize()
        self.title("Course Records Management System")
        self.geometry("1160x720")
        self.minsize(900, 600)
        self.session = None
        self.show_auth()

    def clear(self):
        # Clear ang current screen before magpakita og lain nga screen.
        for child in self.winfo_children():
            child.destroy()

    def show_auth(self):
        # Kung walay Admin pa, setup screen; kung naa na, login screen na.
        self.clear()
        if not auth.admin_exists():
            self.auth_form("setup")
        else:
            self.auth_form("login")

    def auth_form(self, mode):
        # Same form setup para sa Admin setup, login, ug User registration.
        if mode == "login":
            self.login_screen()
            return
        self.configure(fg_color="#F3F6FA")
        title = {"setup": "Initial Admin Setup", "register": "Create User Account"}[mode]
        card = ctk.CTkFrame(self, width=470, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E1E7EF")
        card.place(relx=.5, rely=.5, anchor="center")
        ctk.CTkLabel(card, text="COURSE RECORDS", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2563A6").pack(padx=42, pady=(30, 7))
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=25, weight="bold"), text_color="#172B4D").pack(padx=36, pady=(0, 7))
        if mode == "login":
            ctk.CTkLabel(card, text="Sign in to manage and browse course records.", font=ctk.CTkFont(size=13), text_color="#65758B").pack(padx=24, pady=(0, 17))
        fields = {}
        names = ["Full Name", "Username", "Password", "Confirm Password", "Email"]
        for name in names:
            entry = ctk.CTkEntry(card, width=340, placeholder_text=name, show="•" if "Password" in name else "")
            entry.pack(padx=30, pady=6)
            fields[name] = entry
        def submit():
            # Lahi ang action depende kung login, Admin setup, o registration.
            try:
                role = "Admin" if mode == "setup" else "User"
                auth.register(fields["Full Name"].get(), fields["Username"].get(), fields["Password"].get(), fields["Confirm Password"].get(), fields["Email"].get(), role)
                messagebox.showinfo("Account created", f"{role} account created successfully.", parent=self)
                self.show_auth()
            except ValueError as exc:
                messagebox.showerror("Please check your entry", str(exc), parent=self)
            except Exception as exc:
                messagebox.showerror("Database error", f"Database operation failed. Please try again.\n{exc}", parent=self)
        ctk.CTkButton(card, text="Create Admin Account" if mode == "setup" else "Register", command=submit, width=360, height=44, corner_radius=9, font=ctk.CTkFont(size=14, weight="bold")).pack(padx=30, pady=(16, 10))
        if mode == "register":
            ctk.CTkButton(card, text="Back to Login", fg_color="transparent", text_color="#2563a6", command=lambda: self.auth_form("login")).pack(pady=(0, 20))
        else:
            ctk.CTkLabel(card, text="One-time setup: the first account is the Admin.", text_color="gray").pack(padx=20, pady=(0, 24))

    def login_screen(self):
        # Two-column login layout: project info sa left, sign-in card sa right.
        self.clear()
        self.configure(fg_color="#F2F3F5")
        layout = ctk.CTkFrame(self, fg_color="transparent")
        layout.pack(fill="both", expand=True, padx=32, pady=28)

        info = ctk.CTkFrame(layout, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=(0, 28))
        ctk.CTkLabel(info, text="Welcome to", font=ctk.CTkFont(size=27, weight="bold"), text_color="#263445").pack(anchor="w", pady=(30, 0))
        ctk.CTkLabel(info, text="Course Records", font=ctk.CTkFont(size=36, weight="bold"), text_color="#B32132").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(info, text="A simple way to manage and explore academic course information.", font=ctk.CTkFont(size=15), text_color="#64748B", wraplength=560, justify="left").pack(anchor="w", pady=(0, 24))

        highlights = (
            ("01", "Course catalog", "Keep course IDs, codes, programs, units, and instructor details in one place."),
            ("02", "Quick search and filters", "Find courses by keyword, department, program, semester, or status."),
            ("03", "Role-based access", "Admins manage records. Users can browse and search the catalog."),
        )
        for number, heading, description in highlights:
            card = ctk.CTkFrame(info, fg_color="#FFFFFF", corner_radius=14, border_width=1, border_color="#E4E8EE")
            card.pack(fill="x", pady=7)
            badge = ctk.CTkLabel(card, text=number, width=42, height=42, corner_radius=11, fg_color="#FFF1E7", text_color="#D65A00", font=ctk.CTkFont(size=14, weight="bold"))
            badge.pack(side="left", padx=16, pady=15)
            copy = ctk.CTkFrame(card, fg_color="transparent")
            copy.pack(side="left", fill="x", expand=True, padx=(0, 16), pady=12)
            ctk.CTkLabel(copy, text=heading, font=ctk.CTkFont(size=15, weight="bold"), text_color="#263445").pack(anchor="w")
            ctk.CTkLabel(copy, text=description, font=ctk.CTkFont(size=12), text_color="#64748B", wraplength=450, justify="left").pack(anchor="w", pady=(3, 0))

        panel = ctk.CTkFrame(layout, width=430, fg_color="#FFFFFF", corner_radius=22, border_width=1, border_color="#E4E8EE")
        panel.pack(side="right", fill="y", padx=(0, 4), pady=4)
        panel.pack_propagate(False)
        brand = ctk.CTkFrame(panel, fg_color="transparent")
        brand.pack(pady=(42, 24))
        ctk.CTkLabel(brand, text="CR", width=48, height=48, corner_radius=14, fg_color="#B32132", text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=(0, 11))
        ctk.CTkLabel(brand, text="COURSE RECORDS", font=ctk.CTkFont(size=17, weight="bold"), text_color="#263445").pack(side="left")
        ctk.CTkLabel(panel, text="Sign in", font=ctk.CTkFont(size=27, weight="bold"), text_color="#263445").pack(pady=(0, 4))
        ctk.CTkLabel(panel, text="Use your account to access the course catalog.", font=ctk.CTkFont(size=13), text_color="#778397", wraplength=340).pack(pady=(0, 18))
        ctk.CTkLabel(panel, text="ADMIN & USER ACCESS", fg_color="#F0F2F4", text_color="#596575", corner_radius=16, font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(0, 22), padx=24, ipadx=14, ipady=7)

        fields = {}
        for name, placeholder, masked in (("Username", "Enter your username", False), ("Password", "Enter your password", True)):
            ctk.CTkLabel(panel, text=name, font=ctk.CTkFont(size=13, weight="bold"), text_color="#39475A").pack(anchor="w", padx=42, pady=(8, 5))
            entry = ctk.CTkEntry(panel, width=346, height=44, corner_radius=9, font=ctk.CTkFont(size=14), placeholder_text=placeholder, show="*" if masked else "")
            entry.pack(padx=38)
            fields[name] = entry

        def submit_login():
            # I-check ang credentials; kung sakto, adto sa dashboard.
            try:
                self.session = auth.login(fields["Username"].get(), fields["Password"].get())
                self.dashboard()
            except ValueError as exc:
                messagebox.showerror("Login failed", str(exc), parent=self)
            except Exception as exc:
                messagebox.showerror("Database error", f"Database operation failed. Please try again.\n{exc}", parent=self)

        ctk.CTkButton(panel, text="Log In", command=submit_login, width=346, height=46, corner_radius=9, fg_color="#B32132", hover_color="#941A28", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=38, pady=(22, 12))
        ctk.CTkButton(panel, text="Create User Account", fg_color="transparent", text_color="#B32132", hover_color="#FCEDEF", command=lambda: self.auth_form("register")).pack(pady=(0, 18))
        ctk.CTkLabel(panel, text="Your course records are saved on this device.", font=ctk.CTkFont(size=11), text_color="#8993A2", wraplength=330).pack(side="bottom", pady=22)

    def dashboard(self):
        self.clear()
        # Match ang dashboard colors sa login screen para consistent ang app.
        self.configure(fg_color="#F2F3F5")
        # Ang account role maoy magbuot kung mugawas ba ang Add/Edit/Delete buttons.
        admin = self.session["role"] == "Admin"
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(20, 8))
        ctk.CTkLabel(top, text="Course Records", font=ctk.CTkFont(size=25, weight="bold"), text_color="#263445").pack(side="left")
        ctk.CTkLabel(top, text=f"{self.session['full_name']}  ·  {self.session['role']}", text_color="#536273").pack(side="left", padx=20)
        ctk.CTkButton(top, text="Log out", width=100, height=36, corner_radius=9, fg_color="#B32132", hover_color="#941A28", command=self.logout).pack(side="right")
        stats = courses.statistics()
        summary = ctk.CTkFrame(self, fg_color="transparent")
        summary.pack(fill="x", padx=24, pady=8)
        self.stat_labels = []
        for label, key in (("Total Courses", "total"), ("Active", "active"), ("Inactive", "inactive")):
            box = ctk.CTkFrame(summary, corner_radius=14, fg_color="#FFFFFF", border_width=1, border_color="#E4E8EE")
            box.pack(side="left", fill="x", expand=True, padx=(0, 10))
            ctk.CTkLabel(box, text=label, text_color="gray").pack(anchor="w", padx=14, pady=(10, 0))
            val = ctk.CTkLabel(box, text=str(stats[key]), font=ctk.CTkFont(size=22, weight="bold"))
            val.pack(anchor="w", padx=14, pady=(0, 10)); self.stat_labels.append(val)
        controls = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=14, border_width=1, border_color="#E4E8EE")
        controls.pack(fill="x", padx=24, pady=10)
        self.search = ctk.CTkEntry(controls, placeholder_text="Search ID, code, course, instructor, department, program", width=330)
        self.search.pack(side="left", padx=(0, 8)); self.search.bind("<KeyRelease>", lambda e: self.refresh())
        self.filters = {}
        for key, title in (("department", "Department"), ("academic_program", "Program"), ("semester", "Semester"), ("status", "Status")):
            values = ["All"] + (courses.filter_values()[key] if key in ("department", "academic_program") else list(SEMESTERS if key == "semester" else STATUSES))
            combo = ctk.CTkComboBox(controls, values=values, width=135, command=lambda _, k=key: self.refresh(), fg_color="#FFFFFF", border_color="#D7DEE8", button_color="#40566F", button_hover_color="#30445C", text_color="#263445", dropdown_fg_color="#FFFFFF", dropdown_hover_color="#FFF1E7", dropdown_text_color="#263445")
            combo.set("All"); combo.pack(side="left", padx=3); self.filters[key] = combo
        ctk.CTkButton(controls, text="Reset", width=70, fg_color="#40566F", hover_color="#30445C", command=self.reset).pack(side="left", padx=5)
        if admin:
            ctk.CTkButton(controls, text="＋ Add Course", command=lambda: self.course_dialog()).pack(side="right", padx=5)
            ctk.CTkButton(controls, text="Delete", fg_color="#B32132", hover_color="#941A28", command=self.delete).pack(side="right", padx=5)
            ctk.CTkButton(controls, text="Edit", fg_color="#40566F", hover_color="#30445C", command=self.edit).pack(side="right", padx=5)
        if admin:
            # I-match ang Add Course button sa maroon nga primary action color.
            for control in controls.winfo_children():
                if isinstance(control, ctk.CTkButton) and "Add Course" in control.cget("text"):
                    control.configure(fg_color="#B32132", hover_color="#941A28")
        area = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E4E8EE")
        area.pack(fill="both", expand=True, padx=24, pady=(2, 20))
        cols = ("course_id", "course_code", "course_name", "department", "academic_program", "units", "semester", "school_year", "instructor_name", "status")
        self.table = ttk.Treeview(area, columns=cols, show="headings", selectmode="browse")
        table_style = ttk.Style(self)
        table_style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#263445")
        table_style.configure("Treeview.Heading", background="#F3F5F8", foreground="#263445")
        table_style.map("Treeview", background=[("selected", "#B32132")], foreground=[("selected", "#FFFFFF")])
        labels = ("Course ID", "Code", "Course Name", "Department", "Program", "Units", "Semester", "School Year", "Instructor", "Status")
        widths = (85, 90, 170, 115, 95, 55, 100, 100, 130, 75)
        for col, label, width in zip(cols, labels, widths):
            self.table.heading(col, text=label); self.table.column(col, width=width, minwidth=55, stretch=True)
        yscroll = ttk.Scrollbar(area, orient="vertical", command=self.table.yview); self.table.configure(yscrollcommand=yscroll.set)
        xscroll = ttk.Scrollbar(area, orient="horizontal", command=self.table.xview); self.table.configure(xscrollcommand=xscroll.set)
        self.table.pack(side="left", fill="both", expand=True); yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")
        self.empty = ctk.CTkLabel(self, text="", text_color="gray")
        self.empty.place(relx=.5, rely=.55, anchor="center")
        self.refresh()

    def reset(self):
        # Reset ang search ug filters ngadto sa default.
        self.search.delete(0, "end")
        for combo in self.filters.values(): combo.set("All")
        self.refresh()

    def update_filter_values(self):
        # I-refresh ang department/program options gikan sa saved course records.
        available = courses.filter_values()
        for key in ("department", "academic_program"):
            combo = self.filters[key]
            current = combo.get()
            options = ["All"] + available[key]
            combo.configure(values=options)
            if current not in options:
                combo.set("All")

    def refresh(self):
        # Refresh ang table results ug course totals gikan sa database.
        if not hasattr(self, "table") or not self.table.winfo_exists(): return
        # I-sync pirmi ang filter dropdowns sa latest values sa saved courses.
        self.update_filter_values()
        filters = {k: (v.get() if v.get() != "All" else "") for k, v in self.filters.items()}
        rows = courses.list_courses(self.search.get(), filters)
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", iid=str(row["id"]), values=tuple(row[k] for k in ("course_id", "course_code", "course_name", "department", "academic_program", "units", "semester", "school_year", "instructor_name", "status")))
        self.empty.configure(text="No course records yet. Add a course to get started." if not rows and not self.search.get() else "No matching course records found." if not rows else "")
        s = courses.statistics()
        for lbl, key in zip(self.stat_labels, ("total", "active", "inactive")): lbl.configure(text=str(s[key]))

    def selected_id(self):
        # Kinahanglan pili una og course row before edit/delete.
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select a course", "Please select a course first.", parent=self); return None
        return int(selected[0])

    def edit(self):
        # Get ang selected course details, then open ang edit form.
        record_id = self.selected_id()
        if record_id is None: return
        row = next((r for r in courses.list_courses() if r["id"] == record_id), None)
        if row: self.course_dialog(row)

    def delete(self):
        # Admin ra pwede mo-delete, ug mangayo sa og confirmation.
        if self.session["role"] != "Admin":
            messagebox.showerror("Not allowed", "Only Admins can delete courses.", parent=self); return
        record_id = self.selected_id()
        if record_id is None: return
        if messagebox.askyesno("Confirm deletion", "Are you sure you want to delete this course?", parent=self):
            try: courses.delete_course(record_id); self.update_filter_values(); self.refresh(); messagebox.showinfo("Deleted", "Course deleted successfully.", parent=self)
            except Exception as exc: messagebox.showerror("Delete failed", str(exc), parent=self)

    def course_dialog(self, row=None):
        # Scrollable form ni para add o edit course details.
        if self.session["role"] != "Admin":
            messagebox.showerror("Not allowed", "Only Admins can change course records.", parent=self); return
        dialog = ctk.CTkToplevel(self); dialog.title("Update Course" if row else "Add Course"); dialog.geometry("540x680"); dialog.transient(self); dialog.grab_set()
        content = ctk.CTkScrollableFrame(dialog, width=500, height=640)
        content.pack(fill="both", expand=True, padx=12, pady=12)
        ctk.CTkLabel(content, text="Update Course" if row else "Add Course", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 10))
        fields = {}
        specs = (("course_id","Course ID"),("course_code","Course Code"),("course_name","Course Name"),("department","Department"),("academic_program","Academic Program"),("units","Units"),("semester","Semester"),("school_year","School Year (YYYY-YYYY)"),("instructor_name","Instructor Name"),("status","Course Status"))
        for key, label in specs:
            ctk.CTkLabel(content, text=label).pack(anchor="w", padx=40, pady=(5,0))
            if key == "semester": widget=ctk.CTkComboBox(content, values=list(SEMESTERS), width=440)
            elif key == "status": widget=ctk.CTkComboBox(content, values=list(STATUSES), width=440)
            else: widget=ctk.CTkEntry(content, width=440)
            widget.pack(padx=35, pady=(1,2)); fields[key]=widget
            if row:
                if key in ("semester", "status"): widget.set(row[key])
                else: widget.insert(0, str(row[key]))
            elif key == "status": widget.set("Active")
            elif key == "semester": widget.set(SEMESTERS[0])
        def save():
            # Kuhaa ang form values, validate, save, then refresh ang dashboard.
            try:
                data={key: widget.get() for key,widget in fields.items()}
                courses.save_course(data, row["id"] if row else None)
                dialog.destroy(); self.update_filter_values(); self.refresh(); messagebox.showinfo("Saved", "Course changes saved successfully.", parent=self)
            except (ValueError, Exception) as exc:
                messagebox.showerror("Could not save course", str(exc), parent=dialog)
        ctk.CTkButton(content, text="Save Course", command=save, width=440).pack(pady=14)

    def logout(self):
        # Clear ang login session, then balik sa login/setup screen.
        self.session = None
        for name in ("search", "filters", "table"):
            if hasattr(self, name): delattr(self, name)
        self.show_auth()
