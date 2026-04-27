import hashlib
import time


class Block:

    def __init__(self, index, previous_hash, data):

        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash

        # Generate hash
        self.hash = self.calculate_hash()

    # ===========================
    # HASH GENERATION
    # ===========================
    def calculate_hash(self):

        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    # ===========================
    # PRINT BLOCK (DEBUG)
    # ===========================
    def to_dict(self):

        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }