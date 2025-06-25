from infra.message_brokers.base import BaseMessageBroker
from logic.events.messages import NewMessageRecievedFromBrokerEvent
from logic.init import init_container
from logic.mediator.base import Mediator
from settings.config import Config


async def init_message_broker() -> None:
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def consume_in_background() -> None:
    container = init_container()
    config: Config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    mediator: Mediator = container.resolve(Mediator)

    async for message in message_broker.start_consuming(config.new_messages_recieved_event_topic):
        await mediator.publish([
            NewMessageRecievedFromBrokerEvent(
                message_text=message['message_text'],
                message_oid=message['message_oid'],
                chat_oid=message['chat_oid'],
                is_manager=message['is_manager'],
            ),
        ])


async def close_message_broker() -> None:
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()
