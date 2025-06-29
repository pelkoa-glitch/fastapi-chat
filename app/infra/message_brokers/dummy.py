import asyncio
from dataclasses import dataclass

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class DummyMessageBroker(BaseMessageBroker):
    message_queue: asyncio.Queue = asyncio.Queue()

    async def start(self):
        pass

    async def close(self):
        pass

    async def send_message(self, key: str, topic: str, value: bytes):
        await self.message_queue.put(value)

    async def start_consuming(self, topic: str):
        while True:
            message = await self.message_queue.get()
            yield message

    async def stop_consuming(self, topic: str):
        pass
