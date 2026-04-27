class Transaction:

    def __init__(self, citizen_id, candidate_id):

        self.citizen_id = citizen_id
        self.candidate_id = candidate_id

    # ===========================
    # CONVERT TO DICTIONARY
    # ===========================
    def to_dict(self):

        return {
            "citizen_id": self.citizen_id,
            "candidate_id": self.candidate_id
        }

    # ===========================
    # STRING FORMAT (OPTIONAL)
    # ===========================
    def __str__(self):

        return f"Citizen {self.citizen_id} -> Candidate {self.candidate_id}"