import sqlite3
from database import get_db_connection
from model.claim import Claim


class ClaimDAO:
    def get_all_claims(self):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                """
                SELECT id, claim_id, policy_id, customer_name, vehicle_number, insurance_company,
                       accident_date, incident_location, claim_date, claim_amount, reason, description, status, documents
                FROM claims
                ORDER BY id DESC
                """
            ).fetchall()
            return [
                Claim(
                    id=row["id"],
                    claim_id=row["claim_id"],
                    policy_id=row["policy_id"],
                    customer_name=row["customer_name"],
                    vehicle_number=row["vehicle_number"],
                    insurance_company=row["insurance_company"],
                    accident_date=row["accident_date"],
                    incident_location=row["incident_location"] or "",
                    claim_date=row["claim_date"],
                    claim_amount=row["claim_amount"],
                    reason=row["reason"],
                    description=row["description"],
                    status=row["status"],
                    documents=row["documents"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def create_claim(self, claim: Claim):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO claims (
                    claim_id,
                    policy_id,
                    customer_name,
                    vehicle_number,
                    insurance_company,
                    accident_date,
                    incident_location,
                    claim_date,
                    claim_amount,
                    reason,
                    description,
                    status,
                    documents
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    claim.claim_id,
                    claim.policy_id,
                    claim.customer_name,
                    claim.vehicle_number,
                    claim.insurance_company,
                    claim.accident_date,
                    claim.incident_location,
                    claim.claim_date,
                    claim.claim_amount,
                    claim.reason,
                    claim.description,
                    claim.status,
                    claim.documents,
                ),
            )
            conn.commit()
            claim.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
