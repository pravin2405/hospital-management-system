import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class AppointmentsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.selected_id = None
        self.patient_map = {}
        self.doctor_map = {}

        self.patient_var = tk.StringVar()
        self.doctor_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Scheduled")
        self.notes_var = tk.StringVar()

        form = ttk.LabelFrame(self, text="Appointment Details", padding=15)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Patient").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.patient_combo = ttk.Combobox(form, textvariable=self.patient_var, width=25, state="readonly")
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Doctor").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.doctor_combo = ttk.Combobox(form, textvariable=self.doctor_var, width=25, state="readonly")
        self.doctor_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.date_var, width=25).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Time (e.g. 10:00 AM)").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.time_var, width=25).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Status").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.status_var,
                     values=["Scheduled", "Completed", "Cancelled"],
                     width=22, state="readonly").grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Notes").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.notes_var, width=35).grid(row=2, column=3, padx=5, pady=5, sticky="we")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(btn_frame, text="Book Appointment", command=self.add_appointment).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_appointment).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_appointment).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh Lists", command=self.refresh_dropdowns).pack(side="left", padx=5)

        self._build_table()
        self.refresh_dropdowns()
        self.refresh_table()

    def _build_table(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "patient", "doctor", "date", "time", "status", "notes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        headings = {
            "id": "ID", "patient": "Patient", "doctor": "Doctor", "date": "Date",
            "time": "Time", "status": "Status", "notes": "Notes"
        }
        widths = {"id": 40, "patient": 140, "doctor": 160, "date": 90, "time": 90, "status": 90, "notes": 160}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def refresh_dropdowns(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM patients ORDER BY name")
        patients = cur.fetchall()
        self.patient_map = {f"{pid} - {name}": pid for pid, name in patients}
        self.patient_combo["values"] = list(self.patient_map.keys())

        cur.execute("SELECT id, name, specialization FROM doctors ORDER BY name")
        doctors = cur.fetchall()
        self.doctor_map = {f"{did} - {name} ({spec})": did for did, name, spec in doctors}
        self.doctor_combo["values"] = list(self.doctor_map.keys())

        conn.close()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, d.name, a.appt_date, a.appt_time, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appt_date, a.appt_time
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        self.date_var.set(values[3])
        self.time_var.set(values[4])
        self.status_var.set(values[5])
        self.notes_var.set(values[6])

        for label, pid in self.patient_map.items():
            if values[1] in label:
                self.patient_var.set(label)
                break

        for label, did in self.doctor_map.items():
            if values[2] in label:
                self.doctor_var.set(label)
                break

    def _validate_form(self):
        if self.patient_var.get() not in self.patient_map:
            messagebox.showerror("Validation Error", "Please select a valid patient.")
            return False
        if self.doctor_var.get() not in self.doctor_map:
            messagebox.showerror("Validation Error", "Please select a valid doctor.")
            return False
        if not self.date_var.get().strip():
            messagebox.showerror("Validation Error", "Date is required.")
            return False
        if not self.time_var.get().strip():
            messagebox.showerror("Validation Error", "Time is required.")
            return False
        return True

    def add_appointment(self):
        if not self._validate_form():
            return

        patient_id = self.patient_map[self.patient_var.get()]
        doctor_id = self.doctor_map[self.doctor_var.get()]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO appointments (patient_id, doctor_id, appt_date, appt_time, status, notes) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (patient_id, doctor_id, self.date_var.get().strip(), self.time_var.get().strip(),
             self.status_var.get(), self.notes_var.get().strip())
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment booked successfully.")
        self.clear_form()
        self.refresh_table()

    def update_appointment(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select an appointment from the table first.")
            return
        if not self._validate_form():
            return

        patient_id = self.patient_map[self.patient_var.get()]
        doctor_id = self.doctor_map[self.doctor_var.get()]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE appointments SET patient_id=?, doctor_id=?, appt_date=?, appt_time=?, status=?, notes=? WHERE id=?",
            (patient_id, doctor_id, self.date_var.get().strip(), self.time_var.get().strip(),
             self.status_var.get(), self.notes_var.get().strip(), self.selected_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment updated.")
        self.clear_form()
        self.refresh_table()

    def delete_appointment(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select an appointment from the table first.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this appointment?"):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM appointments WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()

        self.clear_form()
        self.refresh_table()

    def clear_form(self):
        self.selected_id = None
        self.patient_var.set("")
        self.doctor_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.status_var.set("Scheduled")
        self.notes_var.set("")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)