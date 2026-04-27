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

        # Create transaction
        transaction = Transaction(
            citizen_id,
            candidate_id
        )

        # Add block to blockchain
        block = self.blockchain.add_block(
            transaction.to_dict()
        )

        # Return block info
        return {
            "index": block.index,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }

    # ===========================
    # GET FULL BLOCKCHAIN
    # ===========================
    def get_chain(self):

        return self.blockchain.get_chain_data()

    # ===========================
    # CHECK CHAIN VALIDITY
    # ===========================
    def is_chain_valid(self):

        return self.blockchain.is_chain_valid()

    # ===========================
    # RESET BLOCKCHAIN (OPTIONAL)
    # ===========================
    def reset_chain(self):

        self.blockchain = Blockchain()