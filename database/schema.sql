-- ===============================
-- ADMINS TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS admins (

    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ===============================
-- CANDIDATES TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS candidates (

    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,

    first_name TEXT NOT NULL,

    middle_name TEXT,

    last_name TEXT NOT NULL,

    father_name TEXT NOT NULL,

    mother_name TEXT NOT NULL,

    mobile TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    voter_id TEXT UNIQUE NOT NULL,

    address TEXT NOT NULL,

    pincode TEXT NOT NULL,

    photo TEXT,

    signature TEXT,

    emoji_symbol TEXT NOT NULL,

    slogan TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ===============================
-- CITIZENS TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS citizens (

    citizen_id INTEGER PRIMARY KEY AUTOINCREMENT,

    first_name TEXT NOT NULL,

    middle_name TEXT,

    last_name TEXT NOT NULL,

    father_name TEXT NOT NULL,

    mother_name TEXT NOT NULL,

    mobile TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    voter_id TEXT UNIQUE NOT NULL,

    address TEXT NOT NULL,

    pincode TEXT NOT NULL,

    photo TEXT,

    signature TEXT,

    has_voted INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ===============================
-- VOTES TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS votes (

    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,

    citizen_id INTEGER NOT NULL,

    candidate_id INTEGER NOT NULL,

    emoji TEXT,

    vote_hash TEXT,

    ip_address TEXT,

    voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (citizen_id)
    REFERENCES citizens(citizen_id),

    FOREIGN KEY (candidate_id)
    REFERENCES candidates(candidate_id)

);



-- ===============================
-- OTP TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS otp_codes (

    otp_id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT NOT NULL,

    otp_code TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_verified INTEGER DEFAULT 0

);



-- ===============================
-- VOTING SESSION TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS voting_sessions (

    session_id INTEGER PRIMARY KEY AUTOINCREMENT,

    session_token TEXT UNIQUE,

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    is_active INTEGER DEFAULT 1

);



-- ===============================
-- RESULT CACHE TABLE
-- ===============================

CREATE TABLE IF NOT EXISTS results (

    result_id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER,

    total_votes INTEGER DEFAULT 0,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidate_id)
    REFERENCES candidates(candidate_id)

);