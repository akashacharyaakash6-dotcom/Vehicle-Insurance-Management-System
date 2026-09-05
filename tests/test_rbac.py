import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from rbac import is_allowed


class RBACTestCase(unittest.TestCase):
    def test_customer_role(self):
        # Allow /customer/*
        self.assertTrue(is_allowed("customer", "John", "/customer/dashboard"))
        self.assertTrue(is_allowed("customer", "John", "/customer/profile"))
        self.assertTrue(is_allowed("customer", "John", "/customer"))

        # Deny /agent/*
        self.assertFalse(is_allowed("customer", "John", "/agent/dashboard"))
        self.assertFalse(is_allowed("customer", "John", "/agent/claims"))

        # Deny unlisted routes like /admin/*
        self.assertFalse(is_allowed("customer", "John", "/admin/settings"))

    def test_agent_role(self):
        # Allow /agent/*
        self.assertTrue(is_allowed("agent", "Sarah", "/agent/dashboard"))
        self.assertTrue(is_allowed("agent", "Sarah", "/agent/claims"))
        self.assertTrue(is_allowed("agent", "Sarah", "/agent"))

        # Deny /admin/* and /customer/*
        self.assertFalse(is_allowed("agent", "Sarah", "/admin/settings"))
        self.assertFalse(is_allowed("agent", "Sarah", "/customer/dashboard"))

    def test_admin_akash_role(self):
        # Admin with username Akash -> Allow /admin/* and /agent/*
        self.assertTrue(is_allowed("admin", "Akash", "/admin/dashboard"))
        self.assertTrue(is_allowed("admin", "Akash", "/admin/settings"))
        self.assertTrue(is_allowed("admin", "Akash", "/agent/dashboard"))
        self.assertTrue(is_allowed("admin", "Akash", "/agent/claims"))

        # Deny /customer/* or other routes if not explicitly matching rule
        self.assertFalse(is_allowed("admin", "Akash", "/customer/dashboard"))

    def test_admin_other_user(self):
        # Admin with username NOT Akash -> Denied
        self.assertFalse(is_allowed("admin", "Bob", "/admin/dashboard"))
        self.assertFalse(is_allowed("admin", "Bob", "/agent/dashboard"))

    def test_invalid_or_missing_roles(self):
        self.assertFalse(is_allowed("", "Akash", "/admin/dashboard"))
        self.assertFalse(is_allowed(None, "Akash", "/admin/dashboard"))
        self.assertFalse(is_allowed("guest", "Akash", "/agent/dashboard"))


if __name__ == "__main__":
    unittest.main()
