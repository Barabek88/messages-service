from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user_id
from app.services.message_service import MessageService
from app.services.tarantool_message_service import TarantoolMessageService
from app.schemas.message import MessageCreate, DialogMessage
from app.logger import logger
from uuid import UUID

router = APIRouter(prefix="/dialog", tags=["Dialog"])
tarantool_router = APIRouter(prefix="/dialog-tarantool", tags=["Dialog-Tarantool"])


async def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
    return MessageService(db)


def get_tarantool_message_service() -> TarantoolMessageService:
    return TarantoolMessageService()


@router.post("/{user_id}/send", status_code=status.HTTP_200_OK)
async def send_message(
    user_id: UUID,
    message_data: MessageCreate,
    service: MessageService = Depends(get_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"[Citus] Sending message from {current_user_id} to {user_id}")
    await service.send_message(message_data, current_user_id, user_id)
    return {}


@router.get("/{user_id}/list", response_model=list[DialogMessage])
async def get_dialog(
    user_id: UUID,
    service: MessageService = Depends(get_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"[Citus] Getting dialog between {current_user_id} and {user_id}")
    messages = await service.get_conversation(current_user_id, user_id)
    return messages


@tarantool_router.post("/{user_id}/send", status_code=status.HTTP_200_OK)
async def send_message_tarantool(
    user_id: UUID,
    message_data: MessageCreate,
    service: TarantoolMessageService = Depends(get_tarantool_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"[Tarantool] Sending message from {current_user_id} to {user_id}")
    service.send_message(message_data, current_user_id, user_id)
    return {}


@tarantool_router.get("/{user_id}/list", response_model=list[DialogMessage])
async def get_dialog_tarantool(
    user_id: UUID,
    service: TarantoolMessageService = Depends(get_tarantool_message_service),
    current_user_id: UUID = Depends(get_current_user_id),
):
    logger.info(f"[Tarantool] Getting dialog between {current_user_id} and {user_id}")
    messages = service.get_conversation(current_user_id, user_id)
    return messages
