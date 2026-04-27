from flask import Blueprint, request, jsonify

from models.vote_model import (
    cast_vote_db,
    get_vote_by_citizen
)

from models.citizen_model import (
    get_citizen_by_id,
    mark_as_voted
)

from models.candidate_model import (
    get_candidate_by_id
)

from services.blockchain_service import BlockchainService


# ===========================
# BLUEPRINT
# ===========================
vote_bp = Blueprint("vote", __name__)

# ===========================
# INIT BLOCKCHAIN
# ===========================
blockchain = BlockchainService()


# ===========================
# CAST VOTE API
# ===========================
@vote_bp.route("/cast", methods=["POST"])
def cast_vote():

    data = request.get_json()

    # Validate input
    if not data.get("citizen_id") or not data.get("candidate_id"):
        return jsonify({
            "error": "citizen_id and candidate_id required"
        }), 400

    citizen_id = data["citizen_id"]
    candidate_id = data["candidate_id"]

    # ===========================
    # CHECK CITIZEN
    # ===========================
    citizen = get_citizen_by_id(citizen_id)

    if not citizen:
        return jsonify({
            "error": "Citizen not found"
        }), 404

    # Already voted check
    if citizen["has_voted"] == 1:
        return jsonify({
            "error": "Citizen already voted"
        }), 409

    # ===========================
    # CHECK CANDIDATE
    # ===========================
    candidate = get_candidate_by_id(candidate_id)

    if not candidate:
        return jsonify({
            "error": "Candidate not found"
        }), 404

    # ===========================
    # DUPLICATE CHECK
    # ===========================
    existing_vote = get_vote_by_citizen(citizen_id)

    if existing_vote:
        return jsonify({
            "error": "Duplicate vote detected"
        }), 409

    # ===========================
    # STORE VOTE DB
    # ===========================
    vote_id = cast_vote_db({
        "citizen_id": citizen_id,
        "candidate_id": candidate_id
    })

    # ===========================
    # MARK VOTED
    # ===========================
    mark_as_voted(citizen_id)

    # ===========================
    # STORE IN BLOCKCHAIN
    # ===========================
    block = blockchain.store_vote(
        citizen_id,
        candidate_id
    )

    # ===========================
    # RESPONSE
    # ===========================
    return jsonify({
        "message": "Vote cast successfully ✅",
        "vote_id": vote_id,
        "blockchain_block": block
    })


# ===========================
# GET BLOCKCHAIN
# ===========================
@vote_bp.route("/blockchain", methods=["GET"])
def view_blockchain():

    return jsonify({
        "chain": blockchain.get_chain(),
        "valid": blockchain.is_chain_valid()
    })


# ===========================
# GET VOTE BY CITIZEN
# ===========================
@vote_bp.route("/<int:citizen_id>", methods=["GET"])
def get_vote(citizen_id):

    vote = get_vote_by_citizen(citizen_id)

    if not vote:
        return jsonify({
            "error": "Vote not found"
        }), 404

    return jsonify(dict(vote))