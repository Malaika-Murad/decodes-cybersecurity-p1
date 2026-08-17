
import hmac

def constant_time_compare(val_a: bytes, val_b: bytes) -> bool:
    return hmac.compare_digest(val_a, val_b)