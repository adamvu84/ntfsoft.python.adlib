"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "chogia.warning@gmail.com"
GMAIL_PASSWORD = "zghq unzu iylo oxxq"


def send_email(to_email, cc_email, bcc_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = to_email
        msg["Cc"] = cc_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        recipients = [to_email] + cc_email.split(",") + bcc_email.split(",")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, recipients, msg.as_string())
        server.quit()

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
