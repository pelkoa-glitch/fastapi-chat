from datetime import datetime
from typing import Iterable

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.messages import (
    Chat,
    Message,
)
from pydantic import BaseModel


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageScherma(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(
            text=message.text.as_generic_type(),
            oid=message.oid,
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'MessageDetailSchema':
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime
    messages: Iterable[MessageDetailSchema]

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
            messages=[
                MessageDetailSchema.from_entity(message)
                for message in chat.messages
            ],

        )


class GetMessagesQueryResponseSchema(BaseQueryResponseSchema):
    items: list[MessageDetailSchema]
