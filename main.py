from fastapi import FastAPI
#  files import
import router.auth as auth
import models.models as models
from databases.database import  engine
from logs.logs import get_logger


logger = get_logger(__name__)
logger.info("Application startup") 

app = FastAPI() # app

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(auth.router) #

@app.get("/")
def root():
    logger.info("default root")
    return {"message": "Welcome to Online Exams API!"}


