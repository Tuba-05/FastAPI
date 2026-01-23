# app/databases/databases.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DBNAME = os.getenv("DB_DBNAME")
DB_SSL_CA_PATH = os.getenv("DB_SSL_CA_PATH")
# mysql+mysqlconnector://AA:password@host:port/dbname?auth_plugin=mysql_native_password
# mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

engine = create_engine( DATABASE_URL,
                        pool_size=10,
                        max_overflow=20,
                        connect_args={ "ssl_ca": DB_SSL_CA_PATH  # path to your CA certificate
                        }, echo=True  # shows SQL queries in console (use False in production)
)

# 2. Create Session
SessionLocal = sessionmaker(autocommit=False, # Disables automatic transaction commits.
                            autoflush=False, # Ensures changes are not automatically saved to the database. 
                            bind=engine # Connects this session to a specific database engine.
                            )

# 3. Base class for models
model = declarative_base()