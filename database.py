import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vehicle_insurance.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_column(conn, table, column, column_type, default=None):
    existing = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in existing:
        default_clause = f" DEFAULT {default}" if default is not None else ""
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}{default_clause}")


def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                mobile TEXT,
                address TEXT,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                dob TEXT NOT NULL,
                license_no TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id TEXT NOT NULL UNIQUE,
                customer_id TEXT NOT NULL,
                vehicle_number TEXT NOT NULL,
                vehicle_type TEXT DEFAULT 'Car',
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year TEXT NOT NULL,
                registration_date TEXT,
                engine_no TEXT NOT NULL,
                chassis_no TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                policy_id TEXT NOT NULL UNIQUE,
                policy_number TEXT,
                customer_id TEXT NOT NULL,
                vehicle_id TEXT NOT NULL,
                policy_type TEXT NOT NULL,
                premium TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                expiry_date TEXT,
                coverage TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id TEXT NOT NULL UNIQUE,
                user_id TEXT,
                policy_id TEXT NOT NULL,
                vehicle_id TEXT,
                customer_name TEXT,
                vehicle_number TEXT,
                insurance_company TEXT,
                accident_date TEXT NOT NULL,
                incident_location TEXT,
                claim_date TEXT NOT NULL,
                claim_amount TEXT NOT NULL,
                reason TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                documents TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT NOT NULL UNIQUE,
                user_id TEXT NOT NULL,
                policy_id TEXT NOT NULL,
                amount TEXT NOT NULL,
                payment_date TEXT NOT NULL,
                transaction_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
            )
            """
        )
        ensure_column(conn, "users", "user_id", "TEXT")
        ensure_column(conn, "users", "mobile", "TEXT")
        ensure_column(conn, "users", "address", "TEXT")
        ensure_column(conn, "users", "role", "TEXT", default="'customer'")
        ensure_column(conn, "users", "secret_code", "TEXT", default="'AGENT789'")
        ensure_column(conn, "vehicles", "vehicle_type", "TEXT", default="'Car'")
        ensure_column(conn, "vehicles", "registration_date", "TEXT")
        ensure_column(conn, "policies", "policy_number", "TEXT")
        ensure_column(conn, "policies", "expiry_date", "TEXT")
        ensure_column(conn, "claims", "user_id", "TEXT")
        ensure_column(conn, "claims", "vehicle_id", "TEXT")
        ensure_column(conn, "claims", "customer_name", "TEXT")
        ensure_column(conn, "claims", "vehicle_number", "TEXT")
        ensure_column(conn, "claims", "insurance_company", "TEXT")
        ensure_column(conn, "claims", "accident_date", "TEXT")
        ensure_column(conn, "claims", "incident_location", "TEXT")
        ensure_column(conn, "claims", "description", "TEXT")

        # Seed default Agent and Customer if not existing
        agent = conn.execute("SELECT id FROM users WHERE email = 'agent@insurance.com'").fetchone()
        if not agent:
            conn.execute(
                "INSERT INTO users (user_id, username, email, mobile, address, password, role, secret_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("AGT1001", "Insurance Agent Admin", "agent@insurance.com", "9876543210", "Headquarters", "agent123", "agent", "AGENT789"),
            )
        customer = conn.execute("SELECT id FROM users WHERE email = 'john@example.com'").fetchone()
        if not customer:
            conn.execute(
                "INSERT INTO users (user_id, username, email, mobile, address, password, role, secret_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("USR1001", "John Doe", "john@example.com", "9123456789", "742 Evergreen Terrace", "customer123", "customer", ""),
            )
            cust_record = conn.execute("SELECT id FROM customers WHERE customer_id = 'USR1001'").fetchone()
            if not cust_record:
                conn.execute(
                    "INSERT INTO customers (customer_id, name, email, phone, address, dob, license_no) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("USR1001", "John Doe", "john@example.com", "9123456789", "742 Evergreen Terrace", "1992-05-15", "DL-USR1001"),
                )
    conn.close()

