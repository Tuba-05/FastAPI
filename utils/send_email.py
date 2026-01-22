
from logs.logs import get_logger
import smtplib

def send_mail(password, receiver):
    sender = "demotbsx@gmail.com"
    app_password = "rool tnrg ivse sbho"
    email_receiver = receiver
   
   
    message = f"Subject:Forgot password Verification Code\n\nThis is your verification code: {password}" \
    "\n NOTE: this code will be active for 2 minutes."
   
    logger = get_logger(__name__)
    
    try:
        # connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # secure the connection
        server.login(sender, app_password)
        server.sendmail(sender, email_receiver, message)
        
    except Exception as e:
        logger.error("⚠️ Error:", e)
    finally:
        server.quit()