# app/schemas/quizzes_schemas.py

# -------------------------- Pydantic models ---------------------------
from pydantic import BaseModel, Field
from typing import List, Dict

class AddQuestions(BaseModel):
    admin_key: str
    questionText: str
    A : str
    B : str
    C : str
    D : str
    correct_one : str

class TestTaken(BaseModel):
    question_id : int
    answer : str
    