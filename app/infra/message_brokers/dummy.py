from dataclasses import dataclass

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class DummyMessageBroker(BaseMessageBroker):
    async def start(self):
        pass

    async def close(self):
        pass

    async def send_message(self, key: str, topic: str, value: bytes):
        pass

    async def start_consuming(self, topic: str):
        pass

    async def stop_consuming(self, topic: str):
        pass
