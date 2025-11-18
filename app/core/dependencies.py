from app.core.database import AsyncSessionLocal
from fastapi import Request, status
from app.core.jwt_token import get_data_from_jwt_token
from app.core.exceptions import AppError
from app.settings import settings
from uuid import UUID


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(request: Request) -> dict:
    authorization = request.headers.get("authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise AppError("Token missing", status.HTTP_401_UNAUTHORIZED)

    token_parts = authorization.split(" ")
    if len(token_parts) != 2:
        raise AppError("Token missing", status.HTTP_401_UNAUTHORIZED)
    
    token = token_parts[1]
    payload = get_data_from_jwt_token(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    if not payload:
        raise AppError("Token invalid", status.HTTP_401_UNAUTHORIZED)

    return payload


async def get_current_user_id(request: Request) -> UUID:
    user = await get_current_user(request)
    return UUID(user["user_id"])
