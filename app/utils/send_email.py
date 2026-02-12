import smtplib
from email.message import EmailMessage

import os

from dotenv import load_dotenv

load_dotenv()

# senders_email = os.getenv(SENDERS_EMAIL)
# email_password = os.getenv(EMAIl_PASSWORD)

senders_email = "devansh.lamaniya@gammaedge.io"
email_password = "dtgmrgruajxuofkz"

def send_email(to_email: str, subject: str, body: str):
    try:
        print("Using correct email function...")

        msg = EmailMessage()
        msg["From"] = senders_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(senders_email, email_password)
            server.send_message(msg)

        print(f"Email sent to {to_email}")

    except Exception as e:
        print("Email failed:", e)