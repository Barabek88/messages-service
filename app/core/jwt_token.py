from typing import Any, Dict
import jwt
from fastapi import status
from app.core.exceptions import AppError


def get_data_from_jwt_token(token: str, secret_key: str, algorithm: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise AppError("Token expired", status.HTTP_401_UNAUTHORIZED)
    except jwt.PyJWTError:
        raise AppError("Token invalid", status.HTTP_401_UNAUTHORIZED)
