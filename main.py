from fastapi import FastAPI
#  files import
import router
import models.models as models
from databases.database import SessionLocal, engine

app = FastAPI() # app

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(router.routes) #

@app.get("/")
def root():
    return {"message": "Welcome to Online Exams API!"}


