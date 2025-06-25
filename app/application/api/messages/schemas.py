from datetime import datetime

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.messages import (
    Chat,
    ChatListener,
    Message,
)


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


class CreateMessageSchema(BaseModel):
    text: str
    is_manager: bool = False


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str
    is_manager: bool

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(
            text=message.text.as_generic_type(),
            oid=message.oid,
            is_manager=message.is_manager,
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime
    is_manager: bool

    @classmethod
    def from_entity(cls, message: Message) -> 'MessageDetailSchema':
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
            is_manager=message.is_manager,
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )


class AddTelegramListenerSchema(BaseModel):
    telegram_chat_id: str


class AddTelegramListenerResponseSchema(BaseModel):
    listener_id: str

    @classmethod
    def from_entity(cls, listener: ChatListener) -> 'AddTelegramListenerResponseSchema':
        return cls(listener_id=listener.oid)


class GetMessagesQueryResponseSchema(BaseQueryResponseSchema):
    items: list[MessageDetailSchema]


class GetAllChatsQueryResponceSchema(BaseQueryResponseSchema):
    items: list[ChatDetailSchema]


class ChatListenerItemSchema(BaseModel):
    oid: str

    @classmethod
    def from_entity(cls, chat_listener: ChatListener):
        return cls(oid=chat_listener.oid)
