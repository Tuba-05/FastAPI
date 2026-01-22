# app/router/quizzes/questions.py
from fastapi import APIRouter, Depends, HTTPException, Request
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
# files imports
from models.models import Questions, User
from databases.session import get_db
from schemas.quizzes_schemas import AddQuestions
from utils.responses import success_response, error_response
from logs.logs import get_logger
# other imports
from slowapi import Limiter
from slowapi.util import get_remote_address


logger = get_logger(__name__)

# Limiter instance to apply rate limiting based on client IP address
limiter = Limiter(key_func=get_remote_address)

questions_route = APIRouter(prefix="/route", tags=["Route"])

@questions_route.post("online-exams/add-questions/")
@limiter.limit("100/minute")
def add_question( request: Request,questions_data: AddQuestions, db: Session= Depends(get_db)):
    """ takes quiz questions data from admin.
    """ 
    try:
        is_admin = db.query(User).filter(User.admin_secret_key == questions_data.admin_key).first()
        if not is_admin:
            return error_response("You are not allowed to add questions", status_code=403)
        
        quetsions_added= Questions(question_text= questions_data.questionText, option_a= questions_data.option_A, 
                                option_b= questions_data.option_B, option_c= questions_data.option_C, 
                                option_d= questions_data.option_D, correct_option= questions_data.correct_one)
        db.add(quetsions_added)
        db.commit()
        logger.info("Admin added questions to DB.")
        return success_response("Questions successfully added to quiz", data={"question_id": quetsions_added.id}, status_code=201)
        
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

