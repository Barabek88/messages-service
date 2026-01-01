from uuid import UUID
from app.core.tarantool_manager import get_tarantool_connection


class TarantoolMessageRepository:
    def __init__(self):
        self.conn = get_tarantool_connection()

    def create_message(
        self, conversation_id: UUID, sender_id: UUID, receiver_id: UUID, message_text: str
    ) -> dict:
        result = self.conn.call(
            "send_message",
            (str(conversation_id), str(sender_id), str(receiver_id), message_text)
        )
        return result[0]

    def get_conversation(self, conversation_id: UUID, limit: int = 50):
        result = self.conn.call("get_conversation", (str(conversation_id), limit))
        return result[0] if result else []
