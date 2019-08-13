import os
import smtplib

# Here are the email package modules we'll need
from email.message import EmailMessage


class Mail:
    def __init__(self, smtpserver='smtp.gmail.com:587'):
        self.smtp_server = smtpserver

    def send_mail(self, to_address, subject, message):
        server = smtplib.SMTP(self.smtp_server)
        server.starttls()
        server.ehlo()

        email = os.getenv('EMAIL_USERNAME')

        # Next, log in to the server
        server.login(email, os.getenv('EMAIL_PASSWORD'))
        print("MAIL login successful")

        print("MAIL send mail")
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = email
        msg['To'] = to_address
        server.send_message(msg)

        server.close()
