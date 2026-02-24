# here all the CRUD(Db logic) operations will be defined, and then imported into the main.py file to be used in the API endpoints
# sqlalchemy imports
import email
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin, VerifyOtp
from utils.otp import generate_totp, generate_secret, verify_totp
from utils.security import verify_jwt_token, create_access_token, create_refresh_token, security, SECRET_KEY, ALGORITHM
from utils.send_email import send_mail

# other imports
from pwdlib import PasswordHash
import datetime
import jwt

password_hash = PasswordHash.recommended() # creating a password hashing object 

def register_user(db: Session, user_data: UserRegister):
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None, "User with this email already exists."
    
    # 2. Hash the password
    hashed_password = password_hash.hash(user_data.password)
    
    # 3. Create new user object
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        otp_secret=generate_secret()  # Generate a unique OTP secret for the user
    )
    
    # 4. Save to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)
    

def login_user(db: Session, login_data: UserLogin):
    # 1. Fetch user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        return None
    
    # 2. Verify password
    if not password_hash.verify(login_data.password, user.password):
        return None
    
    # 3. Update modified_at (last login)
    user.modified_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user


def logout_user(db: Session, email: UserEmail):
    user = db.query(User).filter(User.email == email.email).first()
    if not user:
        return None, "User not found."
    
    user.modified_at = datetime.utcnow() # update last login time
    try:
        db.commit() # save changes to database
        db.refresh(user)
        return user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def update_password(db: Session, data: PasswordUpdate):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return None, "User not found."
    
    user.password = password_hash.hash(data.new_password)
    user.modified_at = datetime.utcnow()
    valid_otp = verify_totp(user_input= data.otp, secret= user.otp_secret)
    if valid_otp: 
        user.password =  password_hash.hash(data.new_password)
        db.commit()
        db.refresh(user)
    
    try:
        db.commit()
        db.refresh(user)
        return user, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def create_refresh_token_entry(db: Session, user_id: int, token_str: str):
    # Logic to save the token in your new refresh_tokens table
    # (As we discussed in the previous step)
    pass