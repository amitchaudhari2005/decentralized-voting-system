import sqlite3
import os


# ============================
# DATABASE PATH
# ============================

DATABASE_PATH = os.path.join(
    "instance",
    "voting.db"
)


# ============================
# GET CONNECTION
# ============================

def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================
# INITIALIZE DATABASE
# ============================

def init_db():

    # Create instance folder
    os.makedirs("instance", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ============================
    # CANDIDATES TABLE
    # ============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS candidates (

        candidate_id INTEGER
        PRIMARY KEY AUTOINCREMENT,

        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,

        father_name TEXT,
        mother_name TEXT,

        mobile TEXT,
        email TEXT,

        voter_id TEXT,

        address TEXT,
        pincode TEXT,

        photo TEXT,
        signature TEXT,

        emoji_symbol TEXT,
        slogan TEXT

    )

    """)

    # ============================
    # CITIZENS TABLE
    # ============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS citizens (

        citizen_id INTEGER
        PRIMARY KEY AUTOINCREMENT,

        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,

        father_name TEXT,
        mother_name TEXT,

        mobile TEXT,
        email TEXT,

        voter_id TEXT UNIQUE,

        address TEXT,
        pincode TEXT,

        photo TEXT,
        signature TEXT,

        registration_time
        TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ============================
    # VOTES TABLE
    # (Duplicate Prevention)
    # ============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS votes (

        vote_id INTEGER
        PRIMARY KEY AUTOINCREMENT,

        voter_id TEXT UNIQUE,

        candidate_id INTEGER,

        vote_time
        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(candidate_id)
        REFERENCES candidates(candidate_id)

    )

    """)

    conn.commit()
    conn.close()


# ============================
# RESET DATABASE (OPTIONAL)
# ============================

def reset_database():

    if os.path.exists(DATABASE_PATH):

        os.remove(DATABASE_PATH)

    init_db()

    print("Database Reset Successfully!")