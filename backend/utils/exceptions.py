from fastapi import Request, FastAPI
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from utils.responses import success_response, error_response
import logging

logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI):
    
    @app.exception_handler(OperationalError)
    async def operational_error_handler(request: Request, exc: OperationalError):
        logger.critical(f"Database unavailable: {exc}", exc_info=True)
        return error_response(
            status_code=503,
            message="Database is temporarily unavailable. Please try again later.",
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {exc}", exc_info=True)
        return error_response(
            status_code=500,
            message="An internal database error occurred.",
        )

    @app.exception_handler(Exception)
    async def universal_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled server exception")
        return error_response(
            status_code=500,
            message="Internal server error",
        )
