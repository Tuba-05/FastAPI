# app/schemas/classroom_schemas.py

# -------------------------- Pydantic models ---------------------------
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict


class CreateClassroom(BaseModel):
    token_id: str # owner id
    name: str = Field(max_length=100, min_length=1)
    code: str = Field(max_length=8, min_length=4)  # classroom code

class JoinClassroom(BaseModel):
    token_id: str # user id
    code: str = Field(max_length=8, min_length=4)  # classroom code 

