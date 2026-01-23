# app/schemas/auth_schemas.py

# -------------------------- Pydantic models ---------------------------
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict

# Using EmailStr (requires email-validator) ensures valid email formats
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str # password must be at least 8 chars
    admin_secret_key: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password : str
    
class UserEmail(BaseModel):
    email: EmailStr

class PasswordUpdate(BaseModel):
    email: EmailStr
    new_password: str = Field(max_length=10)
    otp : str 

class VerifyOtp(BaseModel):
    user_email : EmailStr
    # otp = str   
