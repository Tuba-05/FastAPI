from fastapi import FastAPI
#  files import
import routes.auth as auth
import routes.quizzes.quiz as quizzes
import routes.quizzes.questions as question
import routes.quizzes.scores as score
import models.models as models
from databases.database import  engine
from logs.logs import get_logger


logger = get_logger(__name__)
logger.info("Application startup") 

app = FastAPI() # app

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(auth.auth_route) #
app.include_router(quizzes.quiz_route)


@app.get("/")
def root():
    logger.info("default root")
    return {"message": "Welcome to Online Exams API!"}


