# app/router/auth.py
import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

# sqlalchemy imports
from sqlalchemy.orm import Session
# files imports
from backend.crud import crud
from crud.crud import login_user, register_user, update_password, logout_user
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin, VerifyOtp
from utils.responses import success_response, error_response
from utils.security import verify_jwt_token, create_access_token, create_refresh_token, security, SECRET_KEY, ALGORITHM
from utils.send_email import send_mail
from utils.otp import generate_totp, generate_secret, verify_totp
from logs.logs import get_logger
# other imports
from pwdlib import PasswordHash
from slowapi import Limiter
from slowapi.util import get_remote_address
import jwt


logger = get_logger(__name__)

# Limiter instance to apply rate limiting based on client IP address
limiter = Limiter(key_func=get_remote_address)

auth_route = APIRouter(prefix="/online-exams", tags=["Route"]) # for authentication-related endpoints

password_hash = PasswordHash.recommended() # creating a password hashing object 

# ---------------- Registeration ---------------------
@auth_route.post("/users/register/" )
@limiter.limit("5/minute")
def register( request: Request, user_data: UserRegister, db: Session = Depends(get_db) ):
    """ Registers a new user.
        Hashes password before saving.
        Rate limited to 5 requests per minute per IP. """
    # saving user
    register_user = register_user(db, user_data)
    if not register_user:
        return error_response(message="User with this email already exists.", status_code=409)

    logger.info("User registered successfully")
    return success_response(message="User registered successfully", data={"email": register_user.new_user.email}, 
                                status_code=201)

# ---------------- Login ---------------------
@auth_route.post("/users/login/")
@limiter.limit("5/minute")  # Limit login attempts to 5 requests per minute per IP
async def login( request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    """ Authenticates a user and returns a JWT access token.
        Steps:
        1. Fetch user by email
        2. Verify password using pwblib
        3. Generate and return JWT token """
    
    login_user = login_user(db, user_data.email, user_data.password)
        
    if not login_user:
        return error_response( message="Invalid email or password", status_code=401,)
        
    # Create JWT token containing user identity data
    access_token = create_access_token(data={"sub": str(login_user.user.id)})

    refresh_token = create_refresh_token({ "user_id": login_user.user.id })

    logger.info("User logged in successfully")
    return success_response("Suceesfully logged in.", data= {"email": login_user.user.email, 
                                                                 "username": login_user.user.name,
                                                                "access_token": access_token,}, 
                                                        status_code=200)


# ---------------- Logout ---------------------
@auth_route.post("/users/logout/")
@limiter.limit("5/minute")
async def logout( request: Request,user_email: UserEmail, db: Session= Depends(get_db)):
        
    logout_user = logout_user(db, user_email.email)
    if not logout_user: 
        return error_response(message= "User not found", status_code= 404)
    
    logger.info("User logged out successfully")
    return success_response("Logged out successfully", data={"email": logout_user.user.email}, status_code=200)
    

# ---------------- Generate Otp ---------------------    
@auth_route.post("/users/otp")
@limiter.limit("7/minute")
async def get_otp(request: Request, user_data: UserEmail, db: Session = Depends(get_db)):
    """ generate otp send to provoded user email """
    
    is_email_valid = db.query(User).filter(User.email == user_data.email).first()
    if not is_email_valid:
        return error_response(message="Invalid email", status_code= 401 )
    otp = generate_totp(secret= is_email_valid.otp_secret)
    mail_accquired = send_mail(otp, is_email_valid.email)
    if mail_accquired:
        logger.info("✅ Email sent successfully!")
        return success_response("Otp has been generated and sent to your email.", status_code=201)
    return error_response("Something went wrong", status_code=404)
    


# ---------------- Update Password ---------------------    
@auth_route.post("/users/update-password")
@limiter.limit("5/minute")
async def update_password(request: Request, user_data: PasswordUpdate, db: Session= Depends(get_db)):
    """ Updates a user's password.
        Rate-limited to prevent brute-force attacks. """

    user_valid = update_password(db, user_data.email)
    if not user_valid:
        return error_response(message="Invalid email", status_code= 401 )
    
    if user_valid:
        logger.info("User password updated successfully")
        return success_response(message="Password updated!", data={"email": user_data.email}, status_code=200)
    return error_response("Something went wrong", status_code=404)
       
 
# ---------------- Refresh Access Token ---------------------
@auth_route.post("/users/refresh")
@limiter.limit("5/minute")
async def refresh_access_token( request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """ Refreshes the access token using a valid refresh token.
        Checks token signature, expiration, and type. """
    # Actual JWT string (refresh token)
    token = credentials.credentials

    try:
        # Decode the JWT using secret key and algorithm
        # This checks: 1. Token signature  2. Token expiry (exp)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Ensure this token is a REFRESH token, not an access token
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create a new short-lived access token
        new_access_token = create_access_token({"user_id": payload["user_id"] })

        # Send new access token back to client
        return success_response("Access token refreshed", data={
                                                            "access_token": new_access_token,
                                                            "token_type": "bearer" },
                                                        status_code=200)

    # If refresh token exists but is expired
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # If token is fake, tampered, or malformed
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@auth_route.post("users/profile")
def get_profile(payload=Depends(verify_jwt_token)):
    """ Protected route to get user profile data from JWT token payload. """
    user_id = payload["sub"]
    return {"user_id": user_id}


