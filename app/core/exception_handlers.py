from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.logger import logger
from app.core.exceptions import AppError
import uuid


async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.error(f"AppError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code, content={"message": exc.message}
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = str(uuid.uuid4())
    logger.error(f"Unexpected error: {str(exc)} | request_id: {request_id}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "request_id": request_id,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Validation error"},
    )
