from dataclasses import (
    dataclass,
    field,
)
from typing import AsyncIterator

import orjson
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict,
        kw_only=True,
    )

    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        self.consumer.unsubscribe()

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()
