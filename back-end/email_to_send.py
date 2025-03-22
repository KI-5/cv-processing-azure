import smtplib
import schedule
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()

#mail credentials
mail_sender = os.getenv("EMAIL_SENDER") 
print("Checking email", mail_sender)
#mail password 
mail_password = os.getenv("EMAIL_PASSWORD")  
print("Checking password", mail_password)
#smtp server
stmp_server = "smtp.gmail.com"
#smtp port
stmp_port = 587

''' 
Method to send follow-up email
@param receiver_email:email of the receiver
@param receiver_name:name of the receiver
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
    msg=MIMEMultipart()
    msg["From"]=mail_sender
    msg["To"]=receiver_email
    msg["Subject"]= subject
    msg.attach(MIMEText(body,"plain"))

    try:
        server=smtplib.SMTP(stmp_server, stmp_port)
        server.starttls()
        server.login(mail_sender, mail_password)
        server.sendmail(mail_sender, receiver_email, msg.as_string())
        server.quit()
        return f"Email sent to {receiver_email}"
    except Exception as e:
        return f"Error sending email: {e}"

'''
Method to schedule Email
@param receiver_email:email of the receiver
@param receiver_name:name of the receiver
'''
def schedule_email(receiver_email, receiver_name):
    schedule.every().day.at("09:00").do(send_followup_email, receiver_email, receiver_name)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# if __name__ == "__main__":
#     # Test email sending immediately
#     result = send_followup_email("inazumalyoko@gmail.com", "John Doe")
#     print(result)
