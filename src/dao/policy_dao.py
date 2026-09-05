import sqlite3
from database import get_db_connection
from model.policy import Policy


class PolicyDAO:
    def _map_row(self, row):
        keys = row.keys()
        return Policy(
            id=row["id"],
            policy_id=row["policy_id"],
            customer_id=row["customer_id"],
            vehicle_id=row["vehicle_id"],
            policy_type=row["policy_type"],
            premium=row["premium"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            coverage=row["coverage"],
            status=row["status"],
            policy_number=row["policy_number"] if "policy_number" in keys and row["policy_number"] else row["policy_id"],
            expiry_date=row["expiry_date"] if "expiry_date" in keys and row["expiry_date"] else row["end_date"],
        )

    def create_policy(self, policy: Policy):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO policies (
                    policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status, policy_number, expiry_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    policy.policy_id,
                    policy.customer_id,
                    policy.vehicle_id,
                    policy.policy_type,
                    policy.premium,
                    policy.start_date,
                    policy.end_date,
                    policy.coverage,
                    policy.status,
                    policy.policy_number or policy.policy_id,
                    policy.expiry_date or policy.end_date,
                ),
            )
            conn.commit()
            policy.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_policies(self):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status, policy_number, expiry_date
                FROM policies
                ORDER BY id DESC
                """
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()

    def get_policies_by_user_id(self, user_id: str):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status, policy_number, expiry_date
                FROM policies
                WHERE customer_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            ).fetchall()
            return [self._map_row(row) for row in rows]
        finally:
            conn.close()

    def find_by_policy_id(self, policy_id: str):
        conn = get_db_connection()
        try:
            row = conn.execute(
                """
                SELECT id, policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status, policy_number, expiry_date
                FROM policies
                WHERE policy_id = ? OR policy_number = ?
                LIMIT 1
                """,
                (policy_id, policy_id)
            ).fetchone()
            if not row:
                return None
            return self._map_row(row)
        finally:
            conn.close()

