import tempfile
import unittest
from pathlib import Path

import app as flask_app
import database


class ClaimsTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        database.DB_PATH = Path(self.temp_db.name)
        database.init_db()
        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    def test_add_claim_and_view(self):
        with self.client.session_transaction() as session:
            session["user_id"] = 1
            session["username"] = "tester"
            session["email"] = "tester@gmail.com"

        response = self.client.post(
            "/claims/add",
            data={
                "claim_id": "CLM1001",
                "policy_id": "POL2026001",
                "customer_name": "Akash Kumar",
                "vehicle_number": "KA01AB1234",
                "claim_type": "Accident",
                "accident_date": "2026-08-11",
                "incident_location": "Bangalore",
                "description": "Front bumper damaged in accident",
                "claim_amount": "₹50,000",
                "status": "Pending",
                "claim_date": "2026-08-11",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CLM1001", response.data)
        self.assertIn(b"Akash Kumar", response.data)
        self.assertIn(b"KA01AB1234", response.data)
        self.assertIn(b"Accident", response.data)
        self.assertIn(b"Bangalore", response.data)
        self.assertIn(b"Pending", response.data)


if __name__ == "__main__":
    unittest.main()
