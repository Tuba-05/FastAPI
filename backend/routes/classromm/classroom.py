# app/router/classroom.py
import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

# sqlalchemy imports
from sqlalchemy.orm import Session
# files imports
from crud.crud import join_classroom, create_classroom
from models.models import User
from databases.session import get_db
from schemas.classroom_schemas import JoinClassroom, CreateClassroom
from utils.responses import success_response, error_response
from logs.logs import get_logger
# other imports
from slowapi import Limiter
from slowapi.util import get_remote_address


logger = get_logger(__name__)

# Limiter instance to apply rate limiting based on client IP address
limiter = Limiter(key_func=get_remote_address)

classroom_route = APIRouter(prefix="/online-exams", tags=["Route"]) # for authentication-related endpoints

# ---------------- Classroom ---------------------
# 1. Create classroom route
@classroom_route.post("/classroom/create/")
@limiter.limit("500/minute")
async def created_classroom( request: Request, classroom_data: CreateClassroom, db: Session = Depends(get_db)):
    """ Creates a new classroom.
        Steps:
        1. Validate input data
        2. Create classroom entry in database
        3. Return success response """
    classroom = create_classroom(db, classroom_data)
    if not classroom:
        return error_response(message="Failed to create classroom.", status_code=400)
    
    logger.info("Classroom created successfully")
    return success_response(message="Classroom created successfully", data={"classroom_id": classroom.id}, 
                                status_code=201)


# 2. Join classroom route
@classroom_route.post("/classroom/join")
@limiter.limit("2000/minute")
async def joined_classroom( request: Request, classroom_data: JoinClassroom, db: Session = Depends(get_db)):
    """ Creates a new classroom.
        Steps:
        1. Validate input data
        2. Create classroom entry in database
        3. Return success response """
    classroom, error_msg = join_classroom(db, classroom_data)
    if error_msg:
        return error_response(message=error_msg, status_code=400)
    
    logger.info("User joined classroom successfully")
    return success_response(message="User joined classroom successfully", data={"classroom_id": classroom.id}, 
                                status_code=200)

