from fastapi import FastAPI, Request, WebSocket, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# sqlalchemy imports
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
#  files import
from databases.session import get_db
import routes.auth as auth
import routes.quizzes.quiz as quizzes
import routes.quizzes.questions as question
import routes.quizzes.scores as score
import models.models as models
from databases.database import  engine
from logs.logs import get_logger
from web_sockets.exam_socket import exam_room_socket


logger = get_logger(__name__)
logger.info("Application startup") 

app = FastAPI() # app

origins = [ "http://localhost:5173", 
           "http://127.0.0.1:5173",
           ]
# allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods= ["*"],  # Allows all standard methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(auth.auth_route) 
app.include_router(quizzes.quiz_route)
app.include_router(question.questions_route)

print("\n===== REGISTERED ROUTES =====")
for r in app.routes:
    print(r.path)
print("============================\n")



# @app.options("/{path:path}")
# async def options_catch_all():
#     return {}

# --------------- web socktes ---------------
@app.websocket("/ws/exam/{exam_id}")
async def websocket_endpoint(ws: WebSocket, exam_id: int, db: Session = Depends(get_db) ):
    await exam_room_socket(ws, exam_id, db)

# -------------- Route for invalid data format ------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={ "success": False,
                                                    "message": "Email or password is invalid",
                                                    "data": None } )


@app.get("/")
def root():
    logger.info("default root")
    return {"message": "Welcome to Online Exams API!"}


