from services.block import Block


class Blockchain:

    def __init__(self):

        # Blockchain list
        self.chain = []

        # Create first (genesis) block
        self.create_genesis_block()

    # ===========================
    # GENESIS BLOCK
    # ===========================
    def create_genesis_block(self):

        genesis_block = Block(
            index=0,
            previous_hash="0",
            data="Genesis Block"
        )

        self.chain.append(genesis_block)

    # ===========================
    # GET LAST BLOCK
    # ===========================
    def get_latest_block(self):

        return self.chain[-1]

    # ===========================
    # ADD NEW BLOCK
    # ===========================
    def add_block(self, data):

        try:
            previous_block = self.get_latest_block()

            new_block = Block(
                index=len(self.chain),
                previous_hash=previous_block.hash,
                data=data
            )

            self.chain.append(new_block)

            return new_block

        except Exception as e:
            print("add_block error:", e)
            return None

    # ===========================
    # VALIDATE CHAIN
    # ===========================
    def is_chain_valid(self):

        try:
            for i in range(1, len(self.chain)):

                current_block = self.chain[i]
                previous_block = self.chain[i - 1]

                # Check hash integrity
                if current_block.hash != current_block.calculate_hash():
                    return False

                # Check link integrity
                if current_block.previous_hash != previous_block.hash:
                    return False

            return True

        except Exception as e:
            print("chain validation error:", e)
            return False

    # ===========================
    # RETURN FULL CHAIN
    # ===========================
    def get_chain_data(self):

        try:
            return [block.to_dict() for block in self.chain]
        except Exception as e:
            print("get_chain_data error:", e)
            return []
