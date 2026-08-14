import sqlite3
from database import get_db_connection
from model.customer import Customer


class CustomerDAO:
    def create_customer(self, customer: Customer):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO customers (
                    customer_id, name, email, phone, address, dob, license_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    customer.customer_id,
                    customer.name,
                    customer.email,
                    customer.phone,
                    customer.address,
                    customer.dob,
                    customer.license_no,
                ),
            )
            conn.commit()
            customer.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_customers(self):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, customer_id, name, email, phone, address, dob, license_no
                FROM customers
                ORDER BY id DESC
                """
            ).fetchall()
            return [
                Customer(
                    id=row["id"],
                    customer_id=row["customer_id"],
                    name=row["name"],
                    email=row["email"],
                    phone=row["phone"],
                    address=row["address"],
                    dob=row["dob"],
                    license_no=row["license_no"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def find_by_customer_id(self, customer_id: str):
        conn = get_db_connection()
        try:
            row = conn.execute(
                """
                SELECT id, customer_id, name, email, phone, address, dob, license_no
                FROM customers
                WHERE customer_id = ?
                LIMIT 1
                """,
                (customer_id,)
            ).fetchone()
            if not row:
                return None
            return Customer(
                id=row["id"],
                customer_id=row["customer_id"],
                name=row["name"],
                email=row["email"],
                phone=row["phone"],
                address=row["address"],
                dob=row["dob"],
                license_no=row["license_no"],
            )
        finally:
            conn.close()
