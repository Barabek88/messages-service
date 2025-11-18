from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user_id
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate, DialogMessage
from app.logger import logger
from uuid import UUID

router = APIRouter(prefix="/dialog", tags=["Dialog"])


async def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
    return MessageService(db)


@router.post("/{user_id}/send", status_code=status.HTTP_200_OK)
async def send_message(
    user_id: UUID,
    message_data: MessageCreate,
    service: MessageService = Depends(get_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"Sending message from {current_user_id} to {user_id}")
    await service.send_message(message_data, current_user_id, user_id)
    return {}


@router.get("/{user_id}/list", response_model=list[DialogMessage])
async def get_dialog(
    user_id: UUID,
    service: MessageService = Depends(get_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"Getting dialog between {current_user_id} and {user_id}")
    messages = await service.get_conversation(current_user_id, user_id)
    return messages
