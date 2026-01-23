# app/router/quizzes/quiz.py
from fastapi import APIRouter, Depends, HTTPException, Request
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import Questions, User
from databases.session import get_db
from schemas.quizzes_schemas import TestTaken
from utils.responses import success_response, error_response
from logs.logs import get_logger
#  other imports
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = get_logger(__name__)

# Limiter instance to apply rate limiting based on client IP address
limiter = Limiter(key_func=get_remote_address)

quiz_route = APIRouter(prefix="/route", tags=["Route"])

@quiz_route.post("online-exams/quizes/")
@limiter.limit("1000/minute")
def quiz( request: Request, quiz_data: TestTaken, db: Session= Depends(get_db)):
    try:
        is_user_valid =  db.query(User).filter(User.email== quiz_data.user_email).first()
        if not is_user_valid:
            logger.info("User is not registered.")
            return error_response("You are not registered yet.", status_code= 404)
        
        is_question_valid = db.query(Questions).filter(Questions.id== quiz_data.question_id, 
                                                       Questions.correct_option == quiz_data.answer).first()
        if not is_question_valid:
            logger.info("User answers the wrong answer")
            return success_response("Wrong Answer.", status_code= 422)
        logger.info("User answers the correct answer")
        return success_response("Correct Answer.", status_code=201)
        
    except OperationalError:
        # Database unavailable
        logger.critical("Database unavailable (OperationalError)", exc_info=True)
        raise HTTPException(status_code=503, detail="Database unavailable")

    except SQLAlchemyError:
        # General database error
        logger.error("Database error (SQLAlchemyError)", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Unexpected errors
        logger.exception("Unhandled server exception")
        return error_response("Internal server error")
    
