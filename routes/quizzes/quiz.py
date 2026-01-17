# app/router/quizzes/quiz.py
from fastapi import APIRouter, Depends, HTTPException
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import Questions
from databases.session import get_db
from schemas.quizzes_schemas import TestTaken
from utils.responses import success_response, error_response
from logs.logs import get_logger

logger = get_logger(__name__)

quiz_route = APIRouter(prefix="/route", tags=["Route"])

@quiz_route.post("online-exams/quizes/")
def quiz(quiz_data: TestTaken, db: Session= Depends(get_db)):
    try:
        is_question_valid = db.query(Questions).filter(id== quiz_data.question_id).first()
        if not is_question_valid:
            raise HTTPException(status_code= 404, detail= "Question does not exist.")
        
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
    