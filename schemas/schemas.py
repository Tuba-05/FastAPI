# app/schemas/schemas.py

# -------------------------- Pydantic models ---------------------------
from pydantic import BaseModel, EmailStr

# Using EmailStr (requires email-validator) ensures valid email formats
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    admin_secret_key: str | None = None

class UserLogout(BaseModel):
    email: EmailStr
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

