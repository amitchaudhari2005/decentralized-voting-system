from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_otp_email(email, otp):

    msg = Message(

        subject="Voting System OTP Verification",

        sender=current_app.config['MAIL_USERNAME'],

        recipients=[email]

    )

    msg.body = f"""

Your OTP for Voting System is:

{otp}

Do not share this OTP.

"""

    mail.send(msg)