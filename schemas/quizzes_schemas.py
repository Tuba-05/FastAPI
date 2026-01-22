# app/schemas/quizzes_schemas.py

# -------------------------- Pydantic models ---------------------------
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict

class AddQuestions(BaseModel):
    admin_key: str
    questionText: str
    option_A : str
    option_B : str
    option_C : str
    option_D : str
    correct_one : str

class TestTaken(BaseModel):
    user_email : EmailStr
    question_id : int
    answer : str 
    