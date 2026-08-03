from tkinter import ttk
from database import get_connection


class DashboardTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=25)

        title = ttk.Label(self, text="Hospital Overview", font=("Segoe UI", 18, "bold"))
        title.pack(pady=(0, 20))

        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill="x")

        self.patient_card = self._make_card(cards_frame, "Total Patients")
        self.doctor_card = self._make_card(cards_frame, "Total Doctors")
        self.appt_card = self._make_card(cards_frame, "Total Appointments")

        self.patient_card["frame"].pack(side="left", expand=True, fill="both", padx=10)
        self.doctor_card["frame"].pack(side="left", expand=True, fill="both", padx=10)
        self.appt_card["frame"].pack(side="left", expand=True, fill="both", padx=10)

        refresh_btn = ttk.Button(self, text="Refresh Dashboard", command=self.refresh)
        refresh_btn.pack(pady=20)

        self.refresh()

    def _make_card(self, parent, label_text):
        frame = ttk.LabelFrame(parent, text=label_text, padding=20)
        value_label = ttk.Label(frame, text="0", font=("Segoe UI", 26, "bold"))
        value_label.pack()
        return {"frame": frame, "label": value_label}

    def refresh(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM patients")
        self.patient_card["label"].config(text=str(cur.fetchone()[0]))

        cur.execute("SELECT COUNT(*) FROM doctors")
        self.doctor_card["label"].config(text=str(cur.fetchone()[0]))

        cur.execute("SELECT COUNT(*) FROM appointments")
        self.appt_card["label"].config(text=str(cur.fetchone()[0]))

        conn.close()