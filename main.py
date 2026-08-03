import tkinter as tk
from tkinter import ttk
from database import init_db, seed_demo_data
from dashboard_tab import DashboardTab
from patients_tab import PatientsTab
from doctors_tab import DoctorsTab
from appointments_tab import AppointmentsTab



def main():
    init_db()
    seed_demo_data()

    window = tk.Tk()
    window.title("Hospital Management System")
    window.geometry("1000x650")

    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    dashboard_tab = DashboardTab(notebook)
    patients_tab = PatientsTab(notebook)
    doctors_tab = DoctorsTab(notebook)
    appointments_tab= AppointmentsTab(notebook)

    notebook.add(dashboard_tab, text="  Dashboard  ")
    notebook.add(patients_tab, text="  Patients  ")
    notebook.add(doctors_tab, text="  Doctors  ")
    notebook.add(appointments_tab, text="  Appointments  ")

    def on_tab_changed(event):
        selected = event.widget.select()
        tab_text = event.widget.tab(selected, "text").strip()
        if tab_text == "Dashboard":
            dashboard_tab.refresh()
        elif tab_text == "Appointments":
            appointments_tab.refresh_dropdowns()

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    window.mainloop()

if __name__ == "__main__":
    main()





