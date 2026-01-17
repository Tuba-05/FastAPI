# app/router/auth.py
from fastapi import APIRouter, Depends, HTTPException
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserEmail, PasswordUpdate, UserLogin
from utils.responses import success_response, error_response
from logs.logs import get_logger
# other imports
from pwdlib import PasswordHash

logger = get_logger(__name__)

auth_route = APIRouter(prefix="/route", tags=["Route"])

password_hash = PasswordHash.recommended() # creating a password hashing object 

# ---------------- Registeration ---------------------
@auth_route.post("online-exams/users/register/" )
def register(user_data: UserRegister, db: Session = Depends(get_db) ):
    
    try: # saving user
        registered_user = User(name = user_data.name, admin_secret_key= user_data.admin_secret_key,
                               email = user_data.email, password = password_hash.hash(user_data.password) )
        print(user_data.name, user_data.email, user_data.password, user_data.admin_secret_key)
        db.add(registered_user)
        db.commit()
        logger.info("User registered successfully")
        return success_response("User registered successfully", data={"email": registered_user.email}, status_code=201)
    
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


# ---------------- Login ---------------------
@auth_route.post("online-exams/users/login/")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        login_user = db.query(User).filter(User.email == user_data.email).first()
        if not login_user:
            raise HTTPException(status_code= 404, detail= "User not found")
        # Verify password using pwblib
        if not password_hash.verify(user_data.password, login_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        
        logger.info("User logged in successfully")
        return success_response("Suceesfully logged in.", data= {"email": login_user.email}, status_code=200)
    
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
async def logout(user_email: UserEmail, db: Session= Depends(get_db)):
    try:
        logout_user = db.query(User).filter(User.email == user_email).first()
        if not logout_user: 
            raise HTTPException(status_code= 404, detail= "User not found")
        db.delete(logout_user)
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
async def update_password(user_data: PasswordUpdate, db: Session= Depends(get_db)):
    try:
        is_user_valid = db.query(User).filter(User.email == user_data.email).first()
        if not is_user_valid:
            raise HTTPException(status_code= 404, detail= "User not found")
        is_user_valid.password = user_data.new_password
        db.commit()
        db.refresh(is_user_valid)
        logger.info("User password updated successfully")
        return success_response("Password updated!", data={"email": user_data.email}, status_code=200)
           
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

