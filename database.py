import sqlite3


def get_connection():
    conn = sqlite3.connect("hospital.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            contact TEXT,
            address TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            contact TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appt_date TEXT NOT NULL,
            appt_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_demo_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO patients (name, age, gender, contact, address) VALUES (?, ?, ?, ?, ?)",
            ("Amit Sharma", 34, "Male", "9876543210", "Pune, MH")
        )

    conn.commit()
    conn.close()