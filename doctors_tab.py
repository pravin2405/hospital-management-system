import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class DoctorsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.selected_id = None

        self.name_var = tk.StringVar()
        self.spec_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        form = ttk.LabelFrame(self, text="Doctor Details", padding=15)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Specialization").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.spec_var, width=25).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Contact").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.contact_var, width=20).grid(row=0, column=5, padx=5, pady=5)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=0, columnspan=6, pady=(10, 0))

        ttk.Button(btn_frame, text="Add Doctor", command=self.add_doctor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_doctor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_doctor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

        self._build_table()
        self.refresh_table()

    def _build_table(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "specialization", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        headings = {"id": "ID", "name": "Name", "specialization": "Specialization", "contact": "Contact"}
        widths = {"id": 40, "name": 180, "specialization": 180, "contact": 130}

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
        cur.execute("SELECT id, name, specialization, contact FROM doctors ORDER BY id")
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
        self.spec_var.set(values[2])
        self.contact_var.set(values[3])

    def _validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Doctor name is required.")
            return False
        if not self.spec_var.get().strip():
            messagebox.showerror("Validation Error", "Specialization is required.")
            return False
        return True

    def add_doctor(self):
        if not self._validate_form():
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO doctors (name, specialization, contact) VALUES (?, ?, ?)",
            (self.name_var.get().strip(), self.spec_var.get().strip(), self.contact_var.get().strip())
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Doctor added successfully.")
        self.clear_form()
        self.refresh_table()

    def update_doctor(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a doctor from the table first.")
            return
        if not self._validate_form():
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE doctors SET name=?, specialization=?, contact=? WHERE id=?",
            (self.name_var.get().strip(), self.spec_var.get().strip(), self.contact_var.get().strip(), self.selected_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Doctor record updated.")
        self.clear_form()
        self.refresh_table()

    def delete_doctor(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select a doctor from the table first.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this doctor record? This will also remove related appointments."):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM doctors WHERE id=?", (self.selected_id,))
        conn.commit()
        conn.close()

        self.clear_form()
        self.refresh_table()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.spec_var.set("")
        self.contact_var.set("")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)