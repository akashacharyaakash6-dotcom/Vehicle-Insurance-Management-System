import sqlite3
from database import get_db_connection
from model.payment import Payment


class PaymentDAO:
    def _map_row(self, row):
        return Payment(
            id=row["id"],
            payment_id=row["payment_id"],
            user_id=row["user_id"],
            policy_id=row["policy_id"],
            amount=row["amount"],
            payment_date=row["payment_date"],
            transaction_id=row["transaction_id"],
            status=row["status"],
        )

    def create_payment(self, payment: Payment):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO payments (
                    payment_id, user_id, policy_id, amount, payment_date, transaction_id, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payment.payment_id,
                    payment.user_id,
                    payment.policy_id,
                    payment.amount,
                    payment.payment_date,
                    payment.transaction_id,
                    payment.status,
                ),
            )
            conn.commit()
            payment.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_payments(self):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, payment_id, user_id, policy_id, amount, payment_date, transaction_id, status
                FROM payments
                ORDER BY id DESC
                """
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()

    def get_payments_by_user_id(self, user_id: str):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, payment_id, user_id, policy_id, amount, payment_date, transaction_id, status
                FROM payments
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()
