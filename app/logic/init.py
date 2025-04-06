from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageRecievedEvent,
)
from infra.message_brokers.base import BaseMessageBroker
from infra.message_brokers.kafka import KafkaMessageBroker
from infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infra.repositories.messages.mongo import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from infra.websockets.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.events.messages import (
    NewChatCreatedEventHandler,
    NewMessageRecievedEventHandler,
    NewMessageRecievedFromBrokerEvent,
    NewMessageRecievedFromBrokerEventHandler,
)
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.messages import (
    GetAllChatsQuery,
    GetAllChatsQueryHandler,
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # Config
    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    # Motor client
    def create_modgodb_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)

    container.register(AsyncIOMotorClient, factory=create_modgodb_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)

    # Repositories
    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
                mongodb_client=client,
                mongodb_db_name=config.mongodb_chat_database,
                mongodb_collection_name=config.mongodb_chat_collection,
        )

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
                mongodb_client=client,
                mongodb_db_name=config.mongodb_chat_database,
                mongodb_collection_name=config.mongodb_messages_collection,
        )

    container.register(BaseChatsRepository, factory=init_chats_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessagesRepository, factory=init_messages_mongodb_repository, scope=Scope.singleton)

    # Command handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    # Query handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)
    container.register(GetAllChatsQueryHandler)

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                group_id=f'chats-{uuid4()}',
                metadata_max_age_ms=30000,
            ),
        )

    # Message broker
    container.register(BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton)
    container.register(BaseConnectionManager, instance=ConnectionManager(), scope=Scope.singleton)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chats_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository),
        )

        # event handlers
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_received_event_handler = NewMessageRecievedEventHandler(
            broker_topic=config.new_messages_recieved_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_recieved_from_broker_event_handler = NewMessageRecievedFromBrokerEventHandler(
            broker_topic=config.new_messages_recieved_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )

        mediator.register_event(
            NewChatCreatedEvent,
            [new_chat_created_event_handler],
        )
        mediator.register_event(
            NewMessageRecievedEvent,
            [new_message_received_event_handler],
        )
        mediator.register_event(
            NewMessageRecievedFromBrokerEvent,
            [new_message_recieved_from_broker_event_handler],
        )
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        mediator.register_query(
            GetAllChatsQuery,
            container.resolve(GetAllChatsQueryHandler),
        )
        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
