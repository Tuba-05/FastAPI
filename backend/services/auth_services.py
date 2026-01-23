# files imports
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin, VerifyOtp
from utils.responses import success_response, error_response
from utils.security import create_access_token, create_refresh_token, security, SECRET_KEY, ALGORITHM
from utils.send_email import send_mail
from utils.otp import generate_totp, generate_secret, verify_totp
from logs.logs import get_logger
# other imports
from pwdlib import PasswordHash
from slowapi import Limiter
from slowapi.util import get_remote_address
import jwt


logger = get_logger(__name__)

def saved_new_user_in_db(name, email, password, admin_key, otp_secret_key):
    """
    Docstring for saved_new_user_in_db
    """