import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email_async(name, email, message):
    try:
        # E-posta gönderim işlemini burada gerçekleştirin
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

        # Create SMTP connection and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.ehlo()

            # mail gönderme işlemi
            server.sendmail(smtp_username, to_address, msg.as_string())
    except Exception as e:
        print(f"An exception occurred: {e}")