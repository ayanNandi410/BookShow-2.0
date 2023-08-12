import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@bookshow.com"
SENDER_PASSWORD = "bookShow123"

def send_email(address,subject,message, attachment=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    if attachment:
        attachment = "files/"+attachment
        with open(attachment, "rb") as attchmt:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attchmt.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment[6:]}",
        )
        msg.attach(part)

    smtp = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    smtp.login(SENDER_ADDRESS,SENDER_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()

    return True