import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
#  files
LOG_FILE = "logs/app.log" 
DB_LOG_FILE = "logs/db.log"
os.makedirs(LOG_DIR, exist_ok=True) # Creates the logs/ directory if it does not exist

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)
# ---------------------------
# App logger (same as yours)
# ---------------------------
# Writes logs to logs/app.log, file size= MB
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        # saves in file
        RotatingFileHandler(
            LOG_FILE, 
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5
        ),
        logging.StreamHandler()  # terminal output
    ]
)
# ---------------------------
# DB logger (separate file)
# ---------------------------
db_handler = RotatingFileHandler(
    DB_LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)
db_handler.setFormatter(logging.Formatter(LOG_FORMAT))
db_handler.setLevel(logging.INFO)

db_logger = logging.getLogger("sqlalchemy.engine")
db_logger.setLevel(logging.INFO)
db_logger.addHandler(db_handler)
db_logger.propagate = False  # IMPORTANT: prevent DB logs from app.log

# ---------------------------
# App logger getter
# ---------------------------
def get_logger(name: str):
    return logging.getLogger(name)
