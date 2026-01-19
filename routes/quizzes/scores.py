# app/router/quizzes/scores.py
from fastapi import APIRouter, Depends, HTTPException
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import User
from databases.session import get_db
from schemas.auth_schemas import UserRegister, UserLogout, PasswordUpdate, UserLogin
from utils.responses import success_response, error_response
from logs.logs import get_logger
# other imports
from pwdlib import PasswordHash

logger = get_logger(__name__)