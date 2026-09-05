import tempfile
import unittest
from pathlib import Path

import app as flask_app
import database
from src.dao.payment_dao import PaymentDAO
from src.model.payment import Payment


class PaymentFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        database.DB_PATH = Path(self.temp_db.name)
        database.init_db()
        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    def test_payment_creation_and_listing(self):
        payment_dao = PaymentDAO()
        payment = Payment(
            payment_id="PAY9001",
            user_id="USR1001",
            policy_id="POL1001",
            amount="4500",
            payment_date="2026-08-24",
            transaction_id="TXN998877",
            status="Paid",
        )
        self.assertTrue(payment_dao.create_payment(payment))

        user_payments = payment_dao.get_payments_by_user_id("USR1001")
        self.assertEqual(len(user_payments), 1)
        self.assertEqual(user_payments[0].transaction_id, "TXN998877")


if __name__ == "__main__":
    unittest.main()
