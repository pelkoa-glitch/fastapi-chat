from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias='MONGODB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGODB_DATABASE')
    mongodb_chat_collection: str = Field(default='chat', alias='MONGODB_CHAT_COLLECTION')
    mongodb_messages_collection: str = Field(default='messages', alias='MONGODB_MESSAGES_COLLECTION')

    new_chats_event_topic: str = Field(default='new-chats-topic')
    new_messages_recieved_event_topic: str = Field(default='new-message-recieved-topic')

    kafka_url: str = Field(alias='KAFKA_URL')
