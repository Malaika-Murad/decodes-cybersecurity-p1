import unittest
from core.gatekeeper import GatekeeperValidator
from core.crypto import constant_time_compare

class TestSecurityModule(unittest.TestCase):
    def test_short_password(self):
        strength, _, _ = GatekeeperValidator.evaluate("Pass1!")
        self.assertEqual(strength, "Weak")

    def test_blacklisted_password(self):
        strength, _, feedback = GatekeeperValidator.evaluate("password123")
        self.assertEqual(strength, "Weak")
        self.assertIn("Critical: Known common/leaked password.", feedback)

    def test_strong_password(self):
        strength, entropy, _ = GatekeeperValidator.evaluate("X7#k9!vPq2$Z")
        self.assertEqual(strength, "Strong")
        self.assertGreater(entropy, 55.0)

    def test_constant_time_equality(self):
        self.assertTrue(constant_time_compare(b"secret", b"secret"))
        self.assertFalse(constant_time_compare(b"secret", b"wrong"))

if __name__ == "__main__":
    unittest.main()