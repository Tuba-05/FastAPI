# app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from databases.database import model
from datetime import datetime
from sqlalchemy.orm import relationship

class User(model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # indexing for faster lookups
    admin_secret_key = Column(String(50), nullable=True)  # Only for admin users
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    otp_secret = Column(String(50), nullable= True)
    modified_at = Column(DateTime, default=datetime.utcnow()) # utc, global time zone
    created_at = Column(DateTime, default=datetime.utcnow())
     # Relationship to the tokens table
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(model):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Metadata for security
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False) # if detect suspicious activity, set this to True and invalidate the token immediately

    # Link back to User object
    user = relationship("User", back_populates="refresh_tokens")





# UI and business logic not implemented yet, but can be used to store quiz questions and results in the future
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

