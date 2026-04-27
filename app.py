from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session
)

import os
import uuid
import qrcode
import random

from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from dotenv import load_dotenv

from database.db import init_db, get_connection
from services.blockchain_service import BlockchainService

# ============================
# INIT
# ============================
blockchain = BlockchainService()

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

# ============================
# ENV
# ============================
load_dotenv()

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# ============================
# ADMIN
# ============================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================
# FOLDERS
# ============================
app.config["UPLOAD_FOLDER_PHOTO"] = "static/uploads/candidate_photos"
app.config["UPLOAD_FOLDER_SIGNATURE"] = "static/uploads/candidate_signatures"
app.config["QR_FOLDER"] = "static/qr_codes"

os.makedirs(app.config["UPLOAD_FOLDER_PHOTO"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER_SIGNATURE"], exist_ok=True)
os.makedirs(app.config["QR_FOLDER"], exist_ok=True)

# ============================
# DB INIT
# ============================
init_db()

# =========================================================
# HOME
# =========================================================
@app.route("/")
def home():
    return redirect(url_for("admin_login"))

# =========================================================
# ADMIN LOGIN
# =========================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    error = None

    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid Credentials"

    return render_template("admin/login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

# =========================================================
# DASHBOARD
# =========================================================
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin/dashboard.html")

# =========================================================
# CANDIDATE FLOW
# =========================================================
@app.route("/admin/candidate-count")
def candidate_count():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin/candidate_count.html")


@app.route("/candidate/forms", methods=["POST"])
def candidate_forms():
    count = int(request.form.get("candidate_count"))
    return render_template("admin/candidate_forms.html", count=count)


@app.route("/candidate/save", methods=["POST"])
def save_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        total = len([k for k in request.form.keys() if "first_name_" in k])

        for i in range(total):

            email = request.form.get(f"email_{i}")
            voter_id = request.form.get(f"voter_id_{i}")

            existing = cursor.execute("""
                SELECT 1 FROM candidates WHERE email=? OR voter_id=?
            """, (email, voter_id)).fetchone()

            if existing:
                continue

            photo = request.files.get(f"photo_{i}")
            signature = request.files.get(f"signature_{i}")

            photo_name = ""
            sign_name = ""

            if photo:
                photo_name = str(uuid.uuid4()) + "_" + secure_filename(photo.filename)
                photo.save(os.path.join(app.config["UPLOAD_FOLDER_PHOTO"], photo_name))

            if signature:
                sign_name = str(uuid.uuid4()) + "_" + secure_filename(signature.filename)
                signature.save(os.path.join(app.config["UPLOAD_FOLDER_SIGNATURE"], sign_name))

            cursor.execute("""
                INSERT INTO candidates (
                    first_name, middle_name, last_name,
                    father_name, mother_name,
                    mobile, email, voter_id,
                    address, pincode,
                    photo, signature,
                    emoji_symbol, slogan
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form.get(f"first_name_{i}"),
                request.form.get(f"middle_name_{i}"),
                request.form.get(f"last_name_{i}"),
                request.form.get(f"father_name_{i}"),
                request.form.get(f"mother_name_{i}"),
                request.form.get(f"mobile_{i}"),
                email,
                voter_id,
                request.form.get(f"address_{i}"),
                request.form.get(f"pincode_{i}"),
                photo_name,
                sign_name,
                request.form.get(f"emoji_{i}"),
                request.form.get(f"slogan_{i}")
            ))

        conn.commit()

    finally:
        conn.close()

    return redirect(url_for("generate_qr"))

# =========================================================
# QR
# =========================================================
@app.route("/generate/qr")
def generate_qr():

    token = str(uuid.uuid4())
    link = f"http://127.0.0.1:5000/citizen/{token}"

    img = qrcode.make(link)
    filename = f"{token}.png"

    img.save(os.path.join(app.config["QR_FOLDER"], filename))

    return render_template("admin/generate_qr.html", voting_link=link, qr_filename=filename)

# =========================================================
# CITIZEN
# =========================================================
@app.route("/citizen/<token>")
def citizen_entry(token):
    return render_template("citizen/start.html", token=token)


@app.route("/citizen/register")
def citizen_register():
    token = request.args.get("token")
    if not token:
        return "Invalid Token"
    return render_template("citizen/register.html", token=token)

# =========================================================
# OTP
# =========================================================
@app.route("/send-otp", methods=["POST"])
def send_otp():

    email = request.form.get("email")
    otp = str(random.randint(100000, 999999))

    session["otp"] = otp

    print("OTP:", otp)

    try:
        msg = Message(
            "OTP Verification",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"Your OTP is {otp}"
        mail.send(msg)

    except Exception as e:
        print("Email error:", e)

    return jsonify({"message": "OTP sent"})


@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    otp = request.form.get("otp")

    if otp == session.get("otp"):
        session["otp_verified"] = True
        return jsonify({"message": "verified"})

    return jsonify({"message": "invalid"})

# =========================================================
# SAVE CITIZEN
# =========================================================
@app.route("/citizen/save", methods=["POST"])
def save_citizen():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        voter_id = request.form.get("voter_id")

        existing = cursor.execute("""
            SELECT 1 FROM citizens WHERE voter_id=?
        """, (voter_id,)).fetchone()

        if existing:
            return "Already Registered"

        cursor.execute("""
            INSERT INTO citizens (
                first_name, middle_name, last_name,
                father_name, mother_name,
                mobile, email,
                voter_id,
                address, pincode,
                photo, signature
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get("first_name"),
            request.form.get("middle_name"),
            request.form.get("last_name"),
            request.form.get("father_name"),
            request.form.get("mother_name"),
            request.form.get("mobile"),
            request.form.get("email"),
            voter_id,
            request.form.get("address"),
            request.form.get("pincode"),
            "", ""
        ))

        conn.commit()

    finally:
        conn.close()

    return redirect(url_for("show_voting_page"))

# =========================================================
# VOTING
# =========================================================
@app.route("/citizen/voting")
def show_voting_page():

    conn = get_connection()
    cursor = conn.cursor()

    candidates = cursor.execute("SELECT * FROM candidates").fetchall()

    conn.close()

    return render_template("citizen/voting.html", candidates=candidates)

# =========================================================
# VOTE
# =========================================================
@app.route("/vote", methods=["POST"])
def save_vote():

    data = request.get_json()

    voter_id = data.get("voter_id")
    candidate_id = data.get("candidate_id")

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute("""
        SELECT 1 FROM votes WHERE voter_id=?
    """, (voter_id,)).fetchone()

    if existing:
        return jsonify({"message": "Already voted"})

    cursor.execute("""
        INSERT INTO votes (voter_id, candidate_id)
        VALUES (?, ?)
    """, (voter_id, candidate_id))

    conn.commit()

    block = blockchain.store_vote(voter_id, candidate_id)

    conn.close()

    return jsonify({"message": "Vote saved", "block": block})

# =========================================================
# BLOCKCHAIN
# =========================================================
@app.route("/admin/blockchain")
def view_blockchain():

    return render_template(
        "admin/blockchain.html",
        chain=blockchain.get_chain(),
        valid=blockchain.is_chain_valid()
    )

# =========================================================
# RESULTS
# =========================================================
@app.route("/admin/results")
def results():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_connection()
    cursor = conn.cursor()

    data = cursor.execute("""
        SELECT candidates.first_name,
               candidates.last_name,
               candidates.emoji_symbol,
               COUNT(votes.vote_id) as total_votes
        FROM candidates
        LEFT JOIN votes
        ON candidates.candidate_id = votes.candidate_id
        GROUP BY candidates.candidate_id
        ORDER BY total_votes DESC
    """).fetchall()

    conn.close()

    return render_template("admin/results.html", results=data)

# =========================================================
# THANK YOU (FIXED)
# =========================================================
@app.route("/thankyou")
def thankyou():
    return render_template("citizen/thankyou.html")

# =========================================================
# RUN (RENDER READY)
# =========================================================
from app import app
import os

# ============================
# RUN (RENDER READY)
# ============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
