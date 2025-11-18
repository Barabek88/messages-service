from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from uuid import UUID


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(
        self, conversation_id: UUID, sender_id: UUID, receiver_id: UUID, message_text: str
    ) -> UUID:
        query = text(
            """
            INSERT INTO messages (conversation_id, sender_id, receiver_id, text)
            VALUES (:conversation_id, :sender_id, :receiver_id, :text)
            RETURNING id
        """
        )

        result = await self.db.execute(
            query,
            {
                "conversation_id": conversation_id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "text": message_text,
            },
        )
        await self.db.commit()
        return result.scalar_one()

    async def get_conversation(self, conversation_id: UUID, limit: int = 50):
        query = text(
            """
            SELECT sender_id as "from", receiver_id as "to", text
            FROM messages
            WHERE conversation_id = :conversation_id
            ORDER BY created_at DESC
            LIMIT :limit
        """
        )

        result = await self.db.execute(
            query, {"conversation_id": conversation_id, "limit": limit}
        )
        rows = result.mappings().fetchall()
        return [dict(row) for row in rows] if rows else []
