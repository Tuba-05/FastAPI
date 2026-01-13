
from sqlalchemy import Column, Integer, String, DateTime
from database import model
from datetime import datetime

class User(model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # indexing for faster lookups
    admin_secret_key = Column(String, nullable=True)  # Only for admin users
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow,) # utc, global time zone
    created_at = Column(DateTime, default=datetime.utcnow)

class Questions(model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)  # e.g., 'A', 'B', 'C', 'D'
    modified_at = Column(DateTime, default=datetime.utcnow,)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizResults(model):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User.id
    total_marks = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

class User(model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # indexing for faster lookups
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow,) # utc, global time zone
    created_at = Column(DateTime, default=datetime.utcnow)

