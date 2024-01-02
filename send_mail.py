import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

global_smtp_connection = None
def get_smtp_connection():
    global global_smtp_connection
    if global_smtp_connection is None or not global_smtp_connection.noop()[0] == 250:
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        global_smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        global_smtp_connection.starttls()
        global_smtp_connection.ehlo()
        global_smtp_connection.login(smtp_username, smtp_password)
    return global_smtp_connection
def send_email_async(name, email, message):
    try:
        server= get_smtp_connection()
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        to_address = os.getenv('TO_ADDRESS')

        subject = 'Web Form Submission'
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

        # Create email
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(smtp_username, to_address, msg.as_string())
    except Exception as e:
        print(f"An exception occurred: {e}")
