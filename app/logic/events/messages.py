from dataclasses import dataclass
from typing import ClassVar

from domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageRecievedEvent,
)
from infra.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import (
    EventHandler,
    IntegrationEvent,
)


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class NewMessageRecievedEventHandler(EventHandler[NewMessageRecievedEvent, None]):
    async def handle(self, event: NewMessageRecievedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )


@dataclass
class NewMessageRecievedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = 'New Message From Broker Received'

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewMessageRecievedFromBrokerEventHandler(EventHandler[NewMessageRecievedFromBrokerEvent, None]):
    async def handle(self, event: NewMessageRecievedFromBrokerEvent) -> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event),
        )
