from services.blockchain import Blockchain
from services.transaction import Transaction


class BlockchainService:

    def __init__(self):
        # Initialize blockchain
        self.blockchain = Blockchain()

    # ===========================
    # STORE VOTE IN BLOCKCHAIN
    # ===========================
    def store_vote(self, citizen_id, candidate_id):

        try:
            # Create transaction
            transaction = Transaction(
                citizen_id,
                candidate_id
            )

            # Add block to blockchain
            block = self.blockchain.add_block(
                transaction.to_dict()
            )

            # Return safe block info
            return {
                "index": getattr(block, "index", None),
                "data": getattr(block, "data", None),
                "hash": getattr(block, "hash", None),
                "previous_hash": getattr(block, "previous_hash", None)
            }

        except Exception as e:
            print("Blockchain store_vote error:", e)
            return None

    # ===========================
    # GET FULL BLOCKCHAIN
    # ===========================
    def get_chain(self):

        try:
            return self.blockchain.get_chain_data()
        except Exception as e:
            print("get_chain error:", e)
            return []

    # ===========================
    # CHECK CHAIN VALIDITY
    # ===========================
    def is_chain_valid(self):

        try:
            return self.blockchain.is_chain_valid()
        except Exception as e:
            print("chain validation error:", e)
            return False

    # ===========================
    # RESET BLOCKCHAIN (OPTIONAL)
    # ===========================
    def reset_chain(self):

        try:
            self.blockchain = Blockchain()
            return True
        except Exception as e:
            print("reset_chain error:", e)
            return False
