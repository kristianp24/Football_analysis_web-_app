import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()


def send_prediction_ready_email(receiver_email):
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")
    print(f"Sender email: {sender_email}")
    print(f"Receiver email: {receiver_email}")
    print(f"Sender password: {sender_password}")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your football video prediction is ready!"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """
    <html>
      <body>
        <p>Hi there,<br>
           Your video prediction has finished successfully.<br>
           You can now view the statistics in the app.<br>
           <br>
            Football Eye Team
           <br>
        </p>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        try:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
            return False
    
    return True
