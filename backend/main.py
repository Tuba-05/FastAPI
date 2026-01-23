from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
#  files import
import routes.auth as auth
import routes.quizzes.quiz as quizzes
import routes.quizzes.questions as question
import routes.quizzes.scores as score
import models.models as models
from databases.database import  engine
from logs.logs import get_logger
from websockets.socket import post_likes_socket


logger = get_logger(__name__)
logger.info("Application startup") 

app = FastAPI() # app

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(auth.auth_route) 
app.include_router(quizzes.quiz_route)
app.include_router(question.questions_route)


# -----
@app.websocket("/ws/post/{post_id}")
async def websocket_endpoint(ws: WebSocket, post_id: int):
    await post_likes_socket(ws, post_id)

# -------------- Route for invalid data format ------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Email or password is invalid",
            "data": None
        }
    )

@app.get("/")
def root():
    logger.info("default root")
    return {"message": "Welcome to Online Exams API!"}


