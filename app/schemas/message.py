from pydantic import BaseModel, Field
from uuid import UUID


class MessageCreate(BaseModel):
    text: str


class DialogMessage(BaseModel):
    from_: UUID = Field(alias="from")
    to: UUID
    text: str

    class Config:
        from_attributes = True
        populate_by_name = True
