import sqlite3
from database import get_db_connection
from model.policy import Policy


class PolicyDAO:
    def create_policy(self, policy: Policy):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO policies (
                    policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                SELECT id, policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status
                FROM policies
                ORDER BY id DESC
                """
            ).fetchall()
            return [
                Policy(
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
                )
                for row in rows
            ]
        finally:
            conn.close()

    def find_by_policy_id(self, policy_id: str):
        conn = get_db_connection()
        try:
            row = conn.execute(
                """
                SELECT id, policy_id, customer_id, vehicle_id, policy_type, premium, start_date, end_date, coverage, status
                FROM policies
                WHERE policy_id = ?
                LIMIT 1
                """,
                (policy_id,)
            ).fetchone()
            if not row:
                return None
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
            )
        finally:
            conn.close()
