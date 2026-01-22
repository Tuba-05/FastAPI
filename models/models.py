# app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime
from databases.database import model
from datetime import datetime

class User(model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # indexing for faster lookups
    admin_secret_key = Column(String(50), nullable=True)  # Only for admin users
    name = Column(String(100), nullable=False)
    email = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    secret_key = Column(String(50), nullable= True)
    modified_at = Column(DateTime, default=datetime.utcnow()) # utc, global time zone
    created_at = Column(DateTime, default=datetime.utcnow())


class Questions(model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(4000), nullable=False)
    option_a = Column(String(50), nullable=False)
    option_b = Column(String(50), nullable=False)
    option_c = Column(String(50), nullable=False)
    option_d = Column(String(50), nullable=False)
    correct_option = Column(String(50), nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow())
    created_at = Column(DateTime, default=datetime.utcnow())


class QuizResults(model):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User.id
    total_marks = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow())
    created_at = Column(DateTime, default=datetime.utcnow())

