from sqlalchemy import Boolean, DateTime, Text, text as sa_text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4, uuid5, NAMESPACE_DNS, UUID as PyUUID
from app.core.database import Base


def get_conversation_id(user1_id: PyUUID, user2_id: PyUUID) -> PyUUID:
    """Generate consistent conversation_id for two users"""
    ids = sorted([str(user1_id), str(user2_id)])
    return uuid5(NAMESPACE_DNS, f"{ids[0]}:{ids[1]}")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    conversation_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    sender_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    receiver_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=sa_text("true"))
