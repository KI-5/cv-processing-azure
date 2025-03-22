import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email credentials
mail_sender = os.getenv("EMAIL_SENDER")
mail_password = os.getenv("EMAIL_PASSWORD")

# SMTP Server
smtp_server = "smtp.gmail.com"
smtp_port = 587


''' 
Method to send follow-up email
@param receiver_email: email of the receiver
@param receiver_name: name of the receiver
@return: success or failure message
'''
def send_followup_email(receiver_email, receiver_name):
    subject = "Your Job Application is Under Review"
    body = f"""
    Hi {receiver_name},

    Thank you for submitting your job application. 
    We have received your CV and it is currently under review. 
    You will be notified once we have updates.

    Best Regards,  
    Metana Team
    """

    msg = MIMEMultipart()
    msg["From"] = mail_sender
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(mail_sender, mail_password)
        server.sendmail(mail_sender, receiver_email, msg.as_string())
        server.quit()
        return f"Email sent to {receiver_email}"
    except Exception as e:
        return f"Error sending email: {e}"
