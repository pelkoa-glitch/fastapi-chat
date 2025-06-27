from enum import Enum

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"
    LOCAL = "local"


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    ENVIRONMENT: Environment = Environment.DEV

    MONGO_DB_CONNECTION_URI: str = Field()
    MONGODB_DATABASE: str = Field(default='chat')
    MONGODB_CHAT_COLLECTION: str = Field(default='chat')
    MONGODB_MESSAGES_COLLECTION: str = Field(default='messages')

    new_chats_event_topic: str = Field(default='new-chats-topic')
    chat_deleted_topic: str = Field(default='chat-deleted-topic')
    new_messages_recieved_event_topic: str = Field(default='new-messages')
    new_listener_added_topic: str = Field(default='listener-added-topic')

    KAFKA_URL: str = Field()

    APM_SETTINGS: dict = {
        'SERVICE_NAME': 'Support Chat',
        'DEBUG': True,
        'SERVER_URL': 'http://apm-server:8200',
        'CAPTURE_HEADERS': True,
        'CAPTURE_BODY': 'all',
    }
