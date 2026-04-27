# 🗳️ Decentralized Voting System using Flask + Blockchain

A secure, transparent, and tamper-proof online voting system built using **Flask (Python)** and **Blockchain technology**.  
This project ensures **one person – one vote**, with OTP verification, QR-based voting access, and immutable vote storage.

🚀 Live Demo

👉 Access the live voting system here:

🔗 https://decentralized-voting-system-zzla.onrender.com


# 📌 Project Overview

Traditional voting systems are vulnerable to:
- Vote manipulation
- Duplicate voting
- Data tampering
- Lack of transparency

This project solves these issues using:
- 🔐 Authentication system (Admin + Citizen)
- 📱 QR Code-based voting access
- 📧 OTP email verification
- ⛓️ Blockchain-based vote storage
- 🧾 Secure database (SQLite)

The system ensures **transparency, security, and integrity** of voting data.

---

# 🚀 Key Features

## 👨‍💼 Admin Panel
- Secure login system
- Add / manage candidates
- View total candidates
- View voting results
- View blockchain ledger
- Generate QR codes for voting
- Monitor system activity

---

## 🧑 Citizen Module
- QR code / token-based entry
- OTP email verification
- Unique voter ID validation
- Cast vote securely
- Prevent duplicate voting
- Thank you confirmation page

---

## ⛓️ Blockchain System
- Each vote stored as a block
- Hash-based linking of blocks
- Immutable vote records
- Chain validation feature
- Prevents tampering or deletion

---

## 📊 Result System
- Real-time vote counting
- Candidate-wise vote aggregation
- Sorted leaderboard (highest votes first)
- Admin dashboard results page

---

## 📧 OTP Authentication
- Email-based OTP system
- Secure voter verification
- Prevents fake users

---

## 📱 QR Code System
- Unique QR generated per election session
- Encodes voting URL/token
- Secure entry point for voters

---

# 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Blockchain | Custom Python Blockchain |
| Email Service | Flask-Mail (SMTP) |
| QR Code | qrcode library |
| File Handling | Werkzeug |
| PDF Export | ReportLab |

---

# 📁 Project Structure
decentralized-voting-system/
│
├── app.py                  # Main Flask application
├── run.py                  # Entry point
├── config.py               # Configuration file
├── requirements.txt        # Dependencies
│
├── database/
│   ├── db.py               # DB connection
│   ├── schema.sql          # Database schema
│   └── seed_data.sql       # Sample data
│
├── models/                 # Database models
├── routes/                 # Route handlers
├── services/
│   ├── blockchain_service.py
│   ├── email_service.py
│   ├── transaction.py
│   └── block.py
│
├── static/
│   ├── css/
│   ├── uploads/
│   └── qr_codes/
│
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── results.html
│   │   ├── blockchain.html
│   │   ├── candidate_forms.html
│   │   ├── candidate_count.html
│   │   ├── login.html
│   │   └── generate_qr.html
│   │
│   ├── citizen/
│   │   ├── start.html
│   │   ├── register.html
│   │   ├── voting.html
│   │   └── thankyou.html
│
└── exports/                # PDF exports
---# ⚙️ Installation Guide## 1️⃣ Clone Repository```bashgit clone https://github.com/amitchaudhari2005/decentralized-voting-system.gitcd decentralized-voting-system

2️⃣ Create Virtual Environment
python -m venv venvvenv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create .env file:
MAIL_SERVER=smtp.gmail.comMAIL_PORT=587MAIL_USERNAME=your_email@gmail.comMAIL_PASSWORD=your_app_password

5️⃣ Run Project
python app.py
Open browser:
http://127.0.0.1:5000

🔐 Admin Credentials
Username: adminPassword: admin123

🧠 How System Works
Step 1: Admin Setup


Admin logs in


Adds candidates


Generates QR code for election


Step 2: Citizen Entry


Citizen scans QR / opens link


Enters voter details


OTP verification sent to email


Step 3: Voting


Citizen logs in


Views candidate list


Casts vote


Step 4: Blockchain Storage


Vote is stored in database


Same vote is also added to blockchain


Hash linked to previous block


Step 5: Result Calculation


Votes are counted in real time


Displayed in admin dashboard



⛓️ Blockchain Working
Each vote becomes a block:
Block:- Index- Voter ID- Candidate ID- Timestamp- Previous Hash- Current Hash
Chain ensures:


No modification possible


Full audit trail


Data integrity



📊 Future Improvements


Smart contract integration (Ethereum / Solidity)


Mobile application (Android/iOS)


Face recognition voting


Cloud deployment (AWS / Render / Railway)


AI fraud detection system


Multi-election support



👨‍💻 Developer
Amit Chaudhari
GitHub: https://github.com/amitchaudhari2005

📜 License
This project is created for educational purposes only.
Free to use and modify.

