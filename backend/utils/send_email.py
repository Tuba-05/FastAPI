
from logs.logs import get_logger
import smtplib
from email.message import EmailMessage


def send_mail(password, receiver):
    sender = "demotbsx@gmail.com"
    app_password = "rool tnrg ivse sbho"
    email_receiver = "demotbsx@gmail.com"
   
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = email_receiver
    msg['Subject'] = "Otp code for password update"
    msg.set_content(f"This is your verification code: {password}\nNOTE: this code will be active for 2 minutes.")

   
    logger = get_logger(__name__)
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()            # Identify yourself to the SMTP server
            server.starttls()        # Secure the connection
            server.ehlo()            # Re-identify after starting TLS
            server.login(sender, app_password)
            server.send_message(msg)
        
    except Exception as e:
        logger.error("⚠️ Error:", e)