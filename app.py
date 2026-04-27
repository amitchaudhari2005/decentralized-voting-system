from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session
)

from database.db import (
    init_db,
    get_connection
)

import os
import uuid
import qrcode
from werkzeug.utils import secure_filename

from flask_mail import Mail
from dotenv import load_dotenv

# ============================
# BLOCKCHAIN IMPORT
# ============================

from services.blockchain_service import BlockchainService

blockchain = BlockchainService()

# ============================
# CREATE APP
# ============================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_secret")

# ============================
# LOAD ENV
# ============================

load_dotenv()

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# ============================
# ADMIN LOGIN CONFIG
# ============================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================
# UPLOAD FOLDERS
# ============================

app.config['UPLOAD_FOLDER_PHOTO'] = "static/uploads/candidate_photos"
app.config['UPLOAD_FOLDER_SIGNATURE'] = "static/uploads/candidate_signatures"
app.config['QR_FOLDER'] = "static/qr_codes"

os.makedirs(app.config['UPLOAD_FOLDER_PHOTO'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_SIGNATURE'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

# ============================
# INIT DATABASE
# ============================

init_db()

# ============================
# ADMIN LOGIN
# ============================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        else:

            error = "Invalid Username or Password"

    return render_template(
        "admin/login.html",
        error=error
    )


@app.route("/admin")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin/dashboard.html")


@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/")
def home():
    return redirect(url_for("admin_login"))

# ============================
# CANDIDATE COUNT
# ============================

@app.route("/admin/candidate-count")
def candidate_count():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template(
        "admin/candidate_count.html"
    )

# ============================
# SHOW CANDIDATE FORMS
# ============================

@app.route("/candidate/forms", methods=["POST"])
def candidate_forms():

    count = int(
        request.form.get("candidate_count")
    )

    return render_template(
        "admin/candidate_forms.html",
        count=count
    )

# ============================
# SAVE CANDIDATES
# ============================

@app.route("/candidate/save", methods=["POST"])
def save_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        total_candidates = len([

            key for key in request.form.keys()

            if key.startswith("first_name_")

        ])

        for i in range(total_candidates):

            email = request.form.get(f"email_{i}")
            voter_id = request.form.get(f"voter_id_{i}")

            existing = cursor.execute("""

                SELECT * FROM candidates
                WHERE email = ?
                OR voter_id = ?

            """, (email, voter_id)).fetchone()

            if existing:
                continue

            photo_file = request.files.get(f"photo_{i}")
            signature_file = request.files.get(f"signature_{i}")

            photo_filename = ""
            signature_filename = ""

            if photo_file and photo_file.filename:

                photo_filename = secure_filename(
                    str(uuid.uuid4()) + "_" +
                    photo_file.filename
                )

                photo_file.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER_PHOTO'],
                        photo_filename
                    )
                )

            if signature_file and signature_file.filename:

                signature_filename = secure_filename(
                    str(uuid.uuid4()) + "_" +
                    signature_file.filename
                )

                signature_file.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER_SIGNATURE'],
                        signature_filename
                    )
                )

            cursor.execute("""

            INSERT INTO candidates (

                first_name,
                middle_name,
                last_name,
                father_name,
                mother_name,
                mobile,
                email,
                voter_id,
                address,
                pincode,
                photo,
                signature,
                emoji_symbol,
                slogan

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
                photo_filename,
                signature_filename,
                request.form.get(f"emoji_{i}"),
                request.form.get(f"slogan_{i}")

            ))

        conn.commit()

    except Exception as e:

        print("ERROR:", e)

    finally:

        conn.close()

    return redirect(url_for("generate_qr"))

# ============================
# GENERATE QR
# ============================
@app.route("/generate/qr")
def generate_qr():

    token = str(uuid.uuid4())

    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    voting_link = f"{BASE_URL}/citizen/{token}"

    qr = qrcode.make(voting_link)

    qr_filename = f"{token}.png"

    qr_path = os.path.join(
        app.config['QR_FOLDER'],
        qr_filename
    )

    qr.save(qr_path)

    return render_template(
        "admin/generate_qr.html",
        voting_link=voting_link,
        qr_filename=qr_filename
    )

# ============================
# CITIZEN ENTRY (QR open hone par)
# ============================

@app.route("/citizen/<token>")
def citizen_entry(token):

    if not token:
        return "Invalid QR Token"

    try:
        return render_template(
            "citizen/start.html",
            token=token
        )
    except Exception as e:
        return f"Page Error: {str(e)}"

# ============================
# CITIZEN REGISTER PAGE
# ============================

@app.route("/citizen/register")
def citizen_register():

    token = request.args.get("token")

    if not token:
        return "⚠️ Invalid QR Token"

    return render_template(
        "citizen/register.html",
        token=token
    )
    # ============================
# SEND OTP
# ============================

@app.route("/send-otp", methods=["POST"])
def send_otp():

    import random

    email = request.form.get("email")

    otp = str(
        random.randint(100000, 999999)
    )

    session["otp"] = otp
    session["otp_email"] = email

    print("OTP Generated:", otp)

    # OPTIONAL EMAIL SEND
    try:

        from flask_mail import Message

        msg = Message(
            subject="Voting System OTP Verification",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.body = f"""

Your OTP for Voting System:

{otp}

Do not share this OTP.

"""

        mail.send(msg)

    except Exception as e:

        print("Email send failed:", e)

    return jsonify({
        "message": "OTP Sent Successfully"
    })
    # ============================
# VERIFY OTP
# ============================

@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    user_otp = request.form.get("otp")

    if user_otp == session.get("otp"):

        session["otp_verified"] = True

        return jsonify({
            "message": "OTP Verified"
        })

    else:

        return jsonify({
            "message": "Invalid OTP"
        })
# ============================
# SAVE CITIZEN
# ============================

@app.route("/citizen/save", methods=["POST"])
def save_citizen():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        voter_id = request.form.get("voter_id")

        # DUPLICATE CHECK

        existing = cursor.execute("""

            SELECT * FROM citizens
            WHERE voter_id = ?

        """, (voter_id,)).fetchone()

        if existing:

            conn.close()

            return "⚠️ This Voter ID already registered!"


        cursor.execute("""

            INSERT INTO citizens (

                first_name,
                middle_name,
                last_name,

                father_name,
                mother_name,

                mobile,
                email,

                voter_id,

                address,
                pincode,

                photo,
                signature

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

            "",
            ""

        ))

        conn.commit()

    except Exception as e:

        print("Citizen Save Error:", e)

    finally:

        conn.close()

    return redirect(url_for("show_voting_page"))

# ============================
# SHOW VOTING PAGE
# ============================

@app.route("/citizen/voting")
def show_voting_page():

    conn = get_connection()
    cursor = conn.cursor()

    candidates = cursor.execute(
        "SELECT * FROM candidates"
    ).fetchall()

    conn.close()

    return render_template(
        "citizen/voting.html",
        candidates=candidates
    )
# ============================
# SAVE VOTE + BLOCKCHAIN
# ============================
@app.route("/vote", methods=["POST"])
def save_vote():

    data = request.get_json()

    candidate_id = data.get("candidate_id")
    voter_id = data.get("voter_id")

    conn = get_connection()
    cursor = conn.cursor()

    existing_vote = cursor.execute("""
        SELECT * FROM votes
        WHERE voter_id = ?
    """, (voter_id,)).fetchone()

    if existing_vote:
        conn.close()
        return jsonify({
            "message": "❌ You have already voted!"
        })

    cursor.execute("""
        INSERT INTO votes (
            voter_id,
            candidate_id
        )
        VALUES (?, ?)
    """, (voter_id, candidate_id))

    conn.commit()

    try:
        block = blockchain.store_vote(voter_id, candidate_id)
    except Exception as e:
        print("Blockchain error:", e)
        block = None

    conn.close()

    return jsonify({
        "message": "✅ Vote Cast Successfully!",
        "blockchain_block": block
    })
# ============================
# VIEW BLOCKCHAIN
# ============================

@app.route("/admin/blockchain")
def view_blockchain():

    chain = blockchain.get_chain()
    valid = blockchain.is_chain_valid()

    return render_template(
        "admin/blockchain.html",
        chain=chain,
        valid=valid
    )
# ============================
# RESULTS PAGE  ✅ YAHAN ADD KARNA HAI
# ============================

@app.route("/admin/results")
def results():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_connection()
    cursor = conn.cursor()

    results = cursor.execute("""

        SELECT 
            candidates.first_name,
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

    return render_template(
        "admin/results.html",
        results=results
    )

# ============================
# THANK YOU PAGE
# ============================

@app.route("/thankyou")
def thankyou():

    return render_template(
        "citizen/thankyou.html"
    )

# RUN
# ============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
