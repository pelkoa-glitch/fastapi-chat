from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from infra.integrations.notifications.dtos import Notification


@dataclass
class BaseNotificationClient(ABC):

    @abstractmethod
    async def format_notification(self, notification: Notification):
        ...

    @abstractmethod
    async def send_notification(self, notification: Notification):
        ...
