from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import models
from dependencies import get_db
from models import User
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from dependencies import get_db
# from passlib.context import CryptContext

password_hash = PasswordHash.recommended() # 
hashed = password_hash.hash("secret") 
verified = password_hash.verify("secret", hashed)
 # to protect passwords

app = FastAPI()

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

# -------------------------- Pydantic model --------------------------
# Using EmailStr (requires email-validator) ensures valid email formats
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    admin_secret_key: str | None = None
@app.post("online-exams/users/register/" )
async def register(user_data= UserRegister , db: Session = Depends(get_db)):
    
    try: # saving user
        # registered_user = User(name = user_data.name, email = user_data.email, password = user_data.password, 
        #                    admin_secret_key= user_data.admin_secret_key)
        print(user_data.name, user_data.email, user_data.password, user_data.admin_secret_key)
        # db.session.add(registered_user)
        # db.session.commit()
        return JSONResponse( cocntent={"statuscode": 201, "message": "User registered successfully"})
    except Exception as e:
        # db.session.rollback()
        return JSONResponse(content={"status_code": 400, "message": "Registration failed", "error": str(e)})


# @app.post("online-exams/users/login/{email}")
# async def login(email: str, db: Session = Depends(get_db)):

#     login_user = db.session.query(User).filter(User.email == email).first()
#     if not login_user:
#         return JSONResponse( content= {"status_code": 404,"message": "User not found"})
    
#     return JSONResponse( content={"status_code": 201, "message": "World"})


# @app.post("online-exams/users/logout/{email}")
# async def logout(email: str):
#     return {"message": "World"}


# @app.get("online-exams/users/profile")
# async def profile():
#     return {"message": "World"}     



app = FastAPI()


