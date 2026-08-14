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
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
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
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year TEXT NOT NULL,
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
                customer_id TEXT NOT NULL,
                vehicle_id TEXT NOT NULL,
                policy_type TEXT NOT NULL,
                premium TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
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
                policy_id TEXT NOT NULL,
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
        ensure_column(conn, "claims", "customer_name", "TEXT")
        ensure_column(conn, "claims", "vehicle_number", "TEXT")
        ensure_column(conn, "claims", "insurance_company", "TEXT")
        ensure_column(conn, "claims", "accident_date", "TEXT")
        ensure_column(conn, "claims", "incident_location", "TEXT")
        ensure_column(conn, "claims", "description", "TEXT")
    conn.close()
