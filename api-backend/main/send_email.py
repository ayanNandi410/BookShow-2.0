import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@bookshow.com"
SENDER_PASSWORD = "bookShow123"

def send_email(address,subject,message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    smtp = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    smtp.login(SENDER_ADDRESS,SENDER_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()

    return True