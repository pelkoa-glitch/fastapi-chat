from domain.entities.messages import Chat
from pydantic import BaseModel


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return CreateChatRequestSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )
