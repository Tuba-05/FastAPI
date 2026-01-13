
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH")

DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

engine = create_engine( DATABASE_URL,
                        connect_args={ "ssl_ca": SSL_CA_PATH  # path to your CA certificate
                        }, echo=True  # shows SQL queries in console (use False in production)
)
# 2. Create Session
SessionLocal = sessionmaker(autocommit=False, # Disables automatic transaction commits.
                            autoflush=False, # Ensures changes are not automatically saved to the database. 
                            bind=engine # Connects this session to a specific database engine.
                            )

# 3. Base class for models
model = declarative_base()