import tempfile
import unittest
from pathlib import Path

import app as flask_app
import database


class CustomerFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        database.DB_PATH = Path(self.temp_db.name)
        database.init_db()
        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    def test_can_add_customer_and_view_it(self):
        with self.client.session_transaction() as session:
            session["user_id"] = 1
            session["username"] = "tester"
            session["email"] = "tester@gmail.com"

        response = self.client.post(
            "/customers/add",
            data={
                "customer_id": "C-1001",
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "phone": "1234567890",
                "address": "123 Main Street",
                "dob": "1990-01-01",
                "license_no": "LIC12345",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alice Johnson", response.data)


if __name__ == "__main__":
    unittest.main()
