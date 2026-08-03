import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class PatientsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.selected_id = None
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Male")
        self.contact_var = tk.StringVar()
        self.address_var = tk.StringVar()

        form = ttk.LabelFrame(self, text="Patient Details", padding=15)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Age").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.age_var, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Gender").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.gender_var, values=["Male", "Female", "Other"],
                     width=10, state="readonly").grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form, text="Contact").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.contact_var, width=25).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Address").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.address_var, width=35).grid(row=1, column=3, columnspan=3, padx=5, pady=5, sticky="we")

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=(10, 0))

        ttk.Button(btn_frame, text="Add Patient", command=self.add_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

        self._build_table()
        self.refresh_table()

    def _build_table(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "age", "gender", "contact", "address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        headings = {
            "id": "ID", "name": "Name", "age": "Age", "gender": "Gender",
            "contact": "Contact", "address": "Address"
        }
        widths = {"id": 40, "name": 150, "age": 50, "gender": 80, "contact": 110, "address": 220}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, gender, contact, address FROM patients ORDER BY id")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.gender_var.set(values[3])
        self.contact_var.set(values[4])
        self.address_var.set(values[5])

    def _validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Patient name is required.")
            return False
        if not self.age_var.get().strip().isdigit():
            messagebox.showerror("Validation Error", "Age must be a valid number.")
            return False
        return True

    def add_patient(self):
        if not self._validate_form():   
            return
       

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO patients (name, age, gender, contact, address) VALUES (?, ?, ?, ?, ?)",
            (self.name_var.get().strip(), int(self.age_var.get()), self.gender_var.get(),
             self.contact_var.get().strip(), self.address_var.get().strip())
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient added successfully.")
        self.clear_form()
        self.refresh_table()

    def update_patient(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a patient from the table first.")
            return
        if not self._validate_form():
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE patients SET name=?, age=?, gender=?, contact=?, address=? WHERE id=?",
            (self.name_var.get().strip(), int(self.age_var.get()), self.gender_var.get(),
             self.contact_var.get().strip(), self.address_var.get().strip(), self.selected_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient record updated.")
        self.clear_form()
        self.refresh_table()

    def delete_patient(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a patient from the table first.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this patient record? This will also remove related appointments."):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()

        self.clear_form()
        self.refresh_table()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.contact_var.set("")
        self.address_var.set("")
        for sel in self.tree.selection():
           self.tree.selection_remove(sel)