import os
import smtplib

# Here are the email package modules we'll need
from email.message import EmailMessage


class Mail:
    def __init__(self, smtpserver='smtp.gmail.com:587'):
        self.server = smtplib.SMTP(smtpserver)
        self.server.starttls()
        self.server.ehlo()

        self.email = os.getenv('EMAIL_USERNAME')

        # Next, log in to the server
        self.server.login(self.email, os.getenv('EMAIL_PASSWORD'))
        print("MAIL login successful")

    def send_mail(self, to_address, subject, message):
        print("MAIL send mail")
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = to_address
        self.server.send_message(msg)
