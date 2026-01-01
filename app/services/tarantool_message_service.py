from app.repositories.tarantool_message_repository import TarantoolMessageRepository
from app.schemas.message import MessageCreate, DialogMessage
from app.models.message import get_conversation_id
from uuid import UUID


class TarantoolMessageService:
    def __init__(self):
        self.repository = TarantoolMessageRepository()

    def send_message(
        self, message_data: MessageCreate, sender_id: UUID, receiver_id: UUID
    ) -> dict:
        conversation_id = get_conversation_id(sender_id, receiver_id)
        return self.repository.create_message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_text=message_data.text
        )

    def get_conversation(self, current_user_id: UUID, other_user_id: UUID):
        conversation_id = get_conversation_id(current_user_id, other_user_id)
        messages = self.repository.get_conversation(conversation_id)
        return [DialogMessage(from_=UUID(msg["from"]), to=UUID(msg["to"]), text=msg["text"]) for msg in messages]
