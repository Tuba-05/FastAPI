# app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from databases.database import model
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class User(model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    admin_secret_key = Column(String(50), nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    otp_secret = Column(String(50), nullable=True)
    # Use lambda to ensure time is calculated at insertion
    modified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

        # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    owned_groups = relationship("Group", back_populates="owner", cascade="all, delete-orphan")
    group_memberships = relationship("GroupMembers", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(model):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    permanent_token = Column(String(255), unique=True, index=True, nullable=False)
    access_token = Column(String(255), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    
    # back_populates matches User.refresh_tokens
    user = relationship("User", back_populates="refresh_tokens")


class Group(model):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    group_name = Column(String(100), unique=True, nullable=False)
    class_code = Column(String(8), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # back_populates matches User.owned_groups
    owner = relationship("User", back_populates="owned_groups")
    # back_populates matches GroupMembers.group
    group_members = relationship("GroupMembers", back_populates="group", cascade="all, delete-orphan")


class GroupMembers(model):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)    
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # back_populates matches User.group_memberships
    user = relationship("User", back_populates="group_memberships")
    # back_populates matches Group.group_members
    group = relationship("Group", back_populates="group_members")

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
    modified_at = Column(DateTime, default=datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


class QuizResults(model):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User.id
    total_marks = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    modified_at = Column(DateTime, default=datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

