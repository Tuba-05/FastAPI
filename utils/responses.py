# app/utils/responses.py

from fastapi import status

def success_response(message: str, data=None):
    return {
        "status": status.HTTP_200_OK,
        "message": message,
        "data": data
    }

def error_response(message: str, status_code=status.HTTP_400_BAD_REQUEST):
    return {
        "status": status_code,
        "message": message,
        "data": None
    }

