# app/router/routes.py
from fastapi import APIRouter, Depends, HTTPException
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import User, Questions, QuizResults
from databases.session import get_db
from schemas.schemas import UserRegister, UserLogin, UserLogout
from schemas.schemas import UserLogin
from utils.responses import success_response, error_response
# other imports
from pwdlib import PasswordHash

router = APIRouter(prefix="/route", tags=["Route"])

password_hash = PasswordHash.recommended()

@router.post("online-exams/users/register/" )
def register(user_data: UserRegister, db: Session = Depends(get_db) ):
    
    try: # saving user
        registered_user = User(name = user_data.name, admin_secret_key= user_data.admin_secret_key,
                               email = user_data.email, password = password_hash.hash(user_data.password) )
        print(user_data.name, user_data.email, user_data.password, user_data.admin_secret_key)
        db.session.add(registered_user)
        db.session.commit()
        return success_response("User registered successfully", data={"email": registered_user.email })
    
    except OperationalError:
        # Database unavailable
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        print("error", e)
        return error_response("Internal server error")


@router.post("online-exams/users/login/")
async def login(user_email: UserLogin, db: Session = Depends(get_db)):
    try:
        login_user = db.session.query(User).filter(User.email == user_email).first()
        if not login_user:
            raise HTTPException(status_code= 404, detail= "User not found")
        return success_response("Suceesfully logged in.", data= {"email": login_user.email})
    
    except OperationalError:
        # Database unavailable
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        print("error", e)
        return error_response("Internal server error")


@router.post("online-exams/users/logout/{email}")
async def logout(user_email: UserLogout, db: Session= Depends(get_db)):
    try:
        logout_user = db.session.query(User).filter(User.email == user_email).first()
        if not logout_user: 
            raise HTTPException(status_code= 404, detail= "User not found")
        db.session.delete(logout_user)
        return success_response("Logged out successfully", data={"email": logout_user.email})
    
    except OperationalError:
        # Database unavailable
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        print("error", e)
        return error_response("Internal server error")


