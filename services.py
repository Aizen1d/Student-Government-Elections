import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv 
load_dotenv()

import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(student_number, student_email, code):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = student_email
    msg['Subject'] = "Verification Code"

    # Design the body of the email
    body = f"""
        <html>
        <body>
            <p>Hello, Student {student_number}</p>
            <p style="margin-top: 0.2em; margin-bottom: 0.2em;">Your verification code is <strong>{code}</strong>.</p>
            <p style="color: black;">This code will expire in 30 minutes.</p>
            <p></p>
            <p style="color: grey;">Please do not reply to this message. If you did not request this verification code, you can ignore this email.</p>
        </body>
        </html>
    """
    
    # Attach the body to the email
    msg.attach(MIMEText(body, 'html'))

    # Send the email
    server.send_message(msg)
    server.quit()