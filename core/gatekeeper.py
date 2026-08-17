
import math
import string
from core.memory_safe import SecureBuffer
from core.crypto import constant_time_compare

class GatekeeperValidator:
    BLACKLIST = {"password", "12345678", "admin123", "welcome123", "password123"}

    @classmethod
    def evaluate(cls, raw_text: str):
        if not raw_text:
            return "None", 0.0, ["Enter a password to evaluate."]

        sec_buf = SecureBuffer(raw_text)
        buf = sec_buf.get_buffer()
        feedback = []

        try:
            length = len(buf)
            has_upper = any(65 <= b <= 90 for b in buf)
            has_lower = any(97 <= b <= 122 for b in buf)
            has_digit = any(48 <= b <= 57 for b in buf)
            has_symbol = any(b in string.punctuation.encode() for b in buf)

            for common_pass in cls.BLACKLIST:
                if constant_time_compare(bytes(buf), common_pass.encode("utf-8")):
                    return "Weak", 0.0, ["Critical: Known common/leaked password."]

            pool_size = 0
            if has_lower: pool_size += 26
            if has_upper: pool_size += 26
            if has_digit: pool_size += 10
            if has_symbol: pool_size += len(string.punctuation)

            entropy = length * math.log2(pool_size) if pool_size > 0 else 0.0

            # Rule diagnostics
            if length < 8:
                feedback.append("• Requires minimum 8 characters.")
            if not has_upper:
                feedback.append("• Add at least one uppercase letter (A-Z).")
            if not has_lower:
                feedback.append("• Add at least one lowercase letter (a-z).")
            if not has_digit:
                feedback.append("• Add at least one number (0-9).")
            if not has_symbol:
                feedback.append("• Add at least one special symbol (!@#$...).")

            # Classification logic
            score = sum([has_upper, has_lower, has_digit, has_symbol])
            if length < 8 or score <= 2 or entropy < 36:
                strength = "Weak"
            elif score == 3 or entropy < 55:
                strength = "Medium"
            else:
                strength = "Strong"
                feedback = ["• Security Gatekeeper Approved: High Entropy."]

            return strength, round(entropy, 2), feedback

        finally:
            #Wipe memory before function exits
            sec_buf.wipe()