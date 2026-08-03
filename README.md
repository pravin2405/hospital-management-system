# Hospital Management System

Built by Pravin Talawar | 2026

A desktop application to manage patient records, doctors, and appointments,
built with **Python (Tkinter)** for the GUI and **SQLite** for local data storage.

## Features

- **Dashboard** — live counts of patients, doctors, and appointments
- **Patients** — add, update, delete, and view patient records
- **Doctors** — add, update, delete, and view doctor records
- **Appointments** — book appointments linking a patient to a doctor, with
  date, time, status (Scheduled / Completed / Cancelled), and notes
- Data persists between runs in a local `hospital.db` SQLite file
- Deleting a patient or doctor automatically removes their related
  appointments (foreign key cascade)
- Demo data is auto-seeded the first time you run the app, so it's
  immediately usable

## How to Run

### 1. Requirements
- Python 3.8 or newer
- Tkinter (usually included with Python; see below if missing)

**Windows / macOS:** Tkinter ships with the standard python.org installer —
nothing extra to do.

**Linux (if you get `ModuleNotFoundError: No module named 'tkinter'`):**
```bash
sudo apt-get install python3-tk
```

### 2. Run the app
```bash
python main.py
```

No other installation is required — SQLite is built into Python's standard
library.

## Project Structure

## Database Schema

**patients**: id, name, age, gender, contact, address
**doctors**: id, name, specialization, contact
**appointments**: id, patient_id (FK), doctor_id (FK), appt_date, appt_time, status, notes

## Tech Stack

- **Python** — core language
- **Tkinter (ttk)** — GUI
- **SQLite** — database, accessed via Python's built-in `sqlite3` module