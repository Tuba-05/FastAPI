# app/utils/responses.py

from fastapi.responses import JSONResponse

def success_response(message: str, data= None, success= True, status_code= 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success" : success,
            "message": message,
            "data": data
        })


def error_response(message: str, success= False, status_code= 400):
    return JSONResponse(
        status_code= status_code,
        content={
        "success": success,
        "message": message,
        "data": None
    })

