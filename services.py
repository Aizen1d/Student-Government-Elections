import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv 
load_dotenv()

from database import SessionLocal
from models import InsertDataQueues

import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_verification_code_email(student_number, student_email, code):
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

def send_pass_code_queue_email(student_number, student_email, pass_code, queue_id):
    try:
        db = SessionLocal()

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = student_email
        msg['Subject'] = "Temporary Password for Voting"

        # Design the body of the email
        body = f"""
            <html>
            <body>
                <p>Hello, Student {student_number}</p>
                <p style="margin-top: 0.2em; margin-bottom: 0.2em;">Your temporary password is <strong>{pass_code}</strong>.</p>
            </body>
            </html>
        """
        
        # Attach the body to the email
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        server.send_message(msg)
        server.quit()

        # Update the database
        current_task = db.query(InsertDataQueues).filter(InsertDataQueues.QueueId == queue_id).first()

        current_task.EmailSent += 1

        if current_task.EmailSent + current_task.EmailFailed == current_task.ToEmailTotal:
            current_task.Status = "Done"

        db.commit()

    except Exception as e:
        print(e)

        current_task.EmailFailed += 1

        if current_task.EmailSent + current_task.EmailFailed == current_task.ToEmailTotal:
            current_task.Status = "Done"

        db.commit()

def send_pass_code_manual_email(student_number, student_email, pass_code):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = student_email
        msg['Subject'] = "Temporary Password for Voting"

        # Design the body of the email
        body = f"""
            <html>
            <body>
                <p>Hello, Student {student_number}</p>
                <p style="margin-top: 0.2em; margin-bottom: 0.2em;">Your temporary password is <strong>{pass_code}</strong>.</p>
            </body>
            </html>
        """
        
        # Attach the body to the email
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(e)

def send_coc_status_email(student_number, student_email, status, role, election_name):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = student_email

    if status == "Approved":
        msg['Subject'] = "Confirmation of Candidacy Approval"
    else:
        msg['Subject'] = "Regret on Candidacy Application"

    accept = f"""
        <html>
        <body>
            <p>Dear, Student {student_number}</p>
            <p style="margin-top: 0.2em; margin-bottom: 0.2em;">Congratulations! We are pleased to inform you that your candidacy for running <strong>{role}</strong> on <strong>{election_name}</strong> has been approved.</p>
            <p style="color: black;">Your enthusiasm and commitment are truly commendable, and we look forward to seeing the positive impact you will make in your role.</p>
        </body>
        </html>
    """

    reject = f"""
        <html>
        <body>
            <p>Dear, Student {student_number}</p>
            <p style="margin-top: 0.2em; margin-bottom: 0.2em;">We appreciate your interest and dedication in applying for the <strong>{role}</strong> position on <strong>{election_name}</strong>.</p>
            <p style="color: black;">After careful consideration, we regret to inform you that your candidacy has not been successful this time.</p>
        </body>
        </html>
    """

    body = ""
    
    if status == "Approved":
        body = accept
    else:
        body = reject

    msg.attach(MIMEText(body, 'html'))

    # Send the email
    server.send_message(msg)
    server.quit()

def send_partylist_status_email(party_email, status, partylist_name, election_name):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = party_email

    if status == "Approved":
        msg['Subject'] = "Confirmation of Partylist Approval"
    else:
        msg['Subject'] = "Regret on Partylist Application"

    accept = f"""
        <html>
        <body>
            <p>Greetings, fellow student</p>
            <p style="margin-top: 0.2em; margin-bottom: 0.2em;">Congratulations! We are pleased to inform you that your partylist <strong>{partylist_name}</strong> on <strong>{election_name}</strong> has been approved.</p>
        </body>
        </html>
    """

    reject = f"""
        <html>
        <body>
            <p>Greetings, fellow student</p>
            <p style="margin-top: 0.2em; margin-bottom: 0.2em;">We appreciate your interest and dedication in applying for the <strong>{partylist_name}</strong> on <strong>{election_name}</strong>.</p>
            <p style="color: black;">After careful consideration, we regret to inform you that your partylist has not been successful this time.</p>
        </body>
        </html>
    """

    body = ""
    
    if status == "Approved":
        body = accept
    else:
        body = reject

    msg.attach(MIMEText(body, 'html'))

    # Send the email
    server.send_message(msg)
    server.quit()