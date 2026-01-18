import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Secret key used to sign and verify JWTs
SECRET_KEY = os.getenv("JWT_key")

# Algorithm used for signing the token
ALGORITHM = "HS256"

# Token validity duration 
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# HTTP Bearer scheme to extract token from Authorization header
# Expected format: Authorization: Bearer <token>
security = HTTPBearer()


# -------------------- JWT CREATION --------------------
# ****** 1. access token ******
def create_access_token(data: dict):
    """ Creates a JWT token with an expiration time.
        Args: data (dict): Data to encode in the token (e.g., user_id, email)
        Returns: str: Encoded JWT token """
    # Copy data to avoid mutating original dict
    to_encode = data.copy()

    # Set token expiration time
    expire = datetime.utc() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire,  "type": "access"})

    # Encode JWT with secret key and algorithm
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


# ****** refresh token *****
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({ "exp": expire, "type": "refresh" })

    # Encode JWT with secret key and algorithm
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


# -------------------- JWT VERIFICATION --------------------
def verify_jwt_token( credentials: HTTPAuthorizationCredentials = Depends(security) ):
    """ Verifies the JWT token sent in the Authorization header.
        Args: credentials (HTTPAuthorizationCredentials): Extracted Bearer token
        Returns: dict: Decoded token payload if valid
        Raises: HTTPException: If token is expired or invalid """
    # Extract token string from Authorization header
    token = credentials.credentials
    try:
        # Decode and verify token signature and expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")

        return payload # Contains user_id, email, etc.

    except jwt.ExpiredSignatureError:
        # Token exists but has expired
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        # Token is malformed or signature is invalid
        raise HTTPException(status_code=401, detail="Invalid token")
