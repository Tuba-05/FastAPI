# this file purpose is to provide database session dependency
from database import SessionLocal
# from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db # provide a database session to the caller
    finally:
        db.close()
