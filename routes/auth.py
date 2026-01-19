# app/router/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin
from utils.responses import success_response, error_response
from utils.security import create_access_token, create_refresh_token, security, SECRET_KEY, ALGORITHM
from logs.logs import get_logger
# other imports
from pwdlib import PasswordHash
from slowapi import Limiter
from slowapi.util import get_remote_address
import jwt


logger = get_logger(__name__)

# Limiter instance to apply rate limiting based on client IP address
limiter = Limiter(key_func=get_remote_address)

auth_route = APIRouter(prefix="/route", tags=["Route"]) # for authentication-related endpoints

password_hash = PasswordHash.recommended() # creating a password hashing object 

# ---------------- Registeration ---------------------
@auth_route.post("online-exams/users/register/" )
@limiter.limit("5/minute")
def register( request: Request, user_data: UserRegister, db: Session = Depends(get_db) ):
    """ Registers a new user.
        Hashes password before saving.
        Rate limited to 5 requests per minute per IP. """
    try: # saving user
        if db.query(User).filter(User.email== user_data.email).first():
            return error_response(message= "User already registered ", status_code=409 )
        
        registered_user = User(name = user_data.name, admin_secret_key= user_data.admin_secret_key,
                               email = user_data.email, password = password_hash.hash(user_data.password) )
        print(user_data.name, user_data.email, user_data.password, user_data.admin_secret_key)
        db.add(registered_user)
        db.commit()
        logger.info("User registered successfully")
        return success_response(message="User registered successfully", data={"email": registered_user.email}, status_code=201)

    except OperationalError:
        # Database unavailable
        logger.critical("Database unavailable (OperationalError)", exc_info=True)
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        logger.error("Database error (SQLAlchemyError)", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception:
        # Unexpected errors
        logger.exception("Unhandled server exception")
        return error_response("Internal server error")


# ---------------- Login ---------------------
@auth_route.post("online-exams/users/login/")
@limiter.limit("5/minute")  # Limit login attempts to 5 requests per minute per IP
async def login( request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    """ Authenticates a user and returns a JWT access token.
        Steps:
        1. Fetch user by email
        2. Verify password using pwblib
        3. Generate and return JWT token """
    try:
        login_user = db.query(User).filter(User.email == user_data.email).first()
        # if not login_user:
        #     return error_response(message= "User not found", status_code= 404)
        
        # Verify password using pwblib
        if not login_user or not password_hash.verify(user_data.password, login_user.password):
            return error_response( message="Invalid email or password", status_code=401,)
        
        # Create JWT token containing user identity data
        access_token = create_access_token({ "user_id": login_user.id, "email": login_user.email })
        
        refresh_token = create_refresh_token({ "user_id": login_user.id })

        logger.info("User logged in successfully")
        return success_response("Suceesfully logged in.", data= {"email": login_user.email, 
                                                                "access_token": access_token,
                                                                "refresh_token": refresh_token, 
                                                                "token_type": "bearer"}, 
                                                        status_code=200)
    except OperationalError:
        # Database unavailable
        logger.critical("Database unavailable (OperationalError)", exc_info=True)
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        logger.error("Database error (SQLAlchemyError)", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        logger.exception("Unhandled server exception")
        return error_response("Internal server error")


# ---------------- Logout ---------------------
@auth_route.post("online-exams/users/logout/")
@limiter.limit("5/minute")
async def logout( request: Request,user_email: UserEmail, db: Session= Depends(get_db)):
    try:
        logout_user = db.query(User).filter(User.email == user_email.email).first()
        if not logout_user: 
            return error_response(message= "User not found", status_code= 404)
        # db.delete(logout_user)
        # db.commit()
        logger.info("User logged out successfully")
        return success_response("Logged out successfully", data={"email": logout_user.email}, status_code=200)
    
    except OperationalError:
        # Database unavailable
        logger.critical("Database unavailable (OperationalError)", exc_info=True)
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        logger.error("Database error (SQLAlchemyError)", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        logger.exception("Unhandled server exception")
        return error_response("Internal server error")
    

# ---------------- Update Password ---------------------    
@auth_route.post("online-exams/users/password")
@limiter.limit("5/minute")
async def update_password(request: Request, user_data: PasswordUpdate, db: Session= Depends(get_db)):
    """ Updates a user's password.
        Rate-limited to prevent brute-force attacks. """
    try:
        is_email_valid = db.query(User).filter(User.email == user_data.email).first()
        if not is_email_valid:
            return error_response(message="Invalid email", status_code= 401 )
        
        is_email_valid.password =  password_hash.hash(user_data.new_password)
        db.commit()
        db.refresh(is_email_valid)
        logger.info("User password updated successfully")
        return success_response(message="Password updated!", data={"email": user_data.email}, status_code=200)
           
    except OperationalError:
        # Database unavailable
        logger.critical("Database unavailable (OperationalError)", exc_info=True)
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        logger.error("Database error (SQLAlchemyError)", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        logger.exception("Unhandled server exception")
        return error_response("Internal server error")


# ---------------- Refresh Access Token ---------------------
@auth_route.post("/online-exams/users/refresh")
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


