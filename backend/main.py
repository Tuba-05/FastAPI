from fastapi import FastAPI, Request, WebSocket, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# sqlalchemy imports
from sqlalchemy.orm import Session
#  files import
from utils.responses import success_response, error_response
from utils.exceptions import add_exception_handlers
from databases.session import get_db
import routes.auth as auth
import routes.quizzes.quiz as quizzes
import routes.quizzes.questions as question
import routes.quizzes.scores as score
import routes.classromm.classroom as classroom
import models.models as models
from databases.database import  engine
from logs.logs import get_logger
# web socket imports
from web_sockets.exam_socket import exam_room_socket
from web_sockets.classroom_socket import classroom_room_socket


logger = get_logger(__name__)
logger.info("Application startup") 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup: runs before the app starts
    db = next(get_db())
    try:
        db.query(models.GroupMembers).update({"is_online": False}, synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Startup reset failed: {e}")
    finally:
        db.close()

    yield  # ← app runs here

    # ✅ Shutdown: runs when app stops (optional, add cleanup here if needed)

# Pass lifespan to FastAPI
app = FastAPI(lifespan=lifespan)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods= ["*"],  # Allows all standard methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

models.model.metadata.create_all(bind=engine) #Creates tables automatically if they don’t exist

app.include_router(auth.auth_route) 
app.include_router(classroom.classroom_route)
app.include_router(quizzes.quiz_route)
app.include_router(question.questions_route)


print("\n===== REGISTERED ROUTES =====")
for r in app.routes:
    print(r.path)
print("============================\n")



# @app.options("/{path:path}")
# async def options_catch_all():
#     return {}

# ----- Reset online status of all users in classrooms on startup -----
@app.on_event("startup")
def reset_online_status():
    db = next(get_db())
    try:
        db.query(models.GroupMembers).update({"is_online": False}, synchronize_session=False)  # ✅
        db.commit()  # ✅ must commit
    except Exception as e:
        db.rollback()  # ✅ rollback on failure
        print(f"Startup reset failed: {e}")
    finally:
        db.close()  # ✅ always close

# --------------- web socktes ---------------
@app.websocket("/ws/exam/{exam_id}")
async def websocket_endpoint(ws: WebSocket, exam_id: int, db: Session = Depends(get_db) ):
    await exam_room_socket(ws, exam_id, db)


@app.websocket("/ws/classroom/{classroom_code}")
async def classroom_websocket_endpoint(ws: WebSocket, classroom_code: str, db: Session = Depends(get_db) ):
    await classroom_room_socket(ws, classroom_code, db)

# -------------- Route for invalid data format ------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(message="Email or password is invalid", status_code=400)


@app.get("/")
def root():
    logger.info("default root")
    return {"message": "Welcome to Online Exams API!"}


