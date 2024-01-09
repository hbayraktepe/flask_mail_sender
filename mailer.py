import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = 587
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.to_address = os.getenv('TO_ADDRESS')


    def send_email(self, name, email, message):
        subject = 'Web Form Submission'
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

        # Create email
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = self.to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Create SMTP connection and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)

                # Send the email
                server.sendmail(self.smtp_username, self.to_address, msg.as_string())

            print("Email sent successfully.")
        except Exception as e:
            print(f"An error occurred while sending email: {e}")
            raise  # Rethrow the exception to be caught in the calling code
