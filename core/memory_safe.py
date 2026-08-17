class SecureBuffer:
    def __init__(self, text: str):
        self.buffer = bytearray(text, "utf-8")

    def get_buffer(self):
        return self.buffer

    def wipe(self):
        """Explicitly overwrite memory buffer with zeroes."""
        for i in range(len(self.buffer)):
            self.buffer[i] = 0