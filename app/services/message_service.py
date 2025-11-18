from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate, DialogMessage
from app.models.message import get_conversation_id
from uuid import UUID


class MessageService:
    def __init__(self, db: AsyncSession):
        self.repository = MessageRepository(db)

    async def send_message(
        self, message_data: MessageCreate, sender_id: UUID, receiver_id: UUID
    ) -> UUID:
        conversation_id = get_conversation_id(sender_id, receiver_id)
        return await self.repository.create_message(
            conversation_id=conversation_id, 
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            message_text=message_data.text
        )

    async def get_conversation(self, current_user_id: UUID, other_user_id: UUID):
        conversation_id = get_conversation_id(current_user_id, other_user_id)
        messages = await self.repository.get_conversation(conversation_id)
        return (
            [DialogMessage.model_validate(msg) for msg in messages] if messages else []
        )
