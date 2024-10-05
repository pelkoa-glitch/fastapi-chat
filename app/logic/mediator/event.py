from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from domain.events.base import BaseEvent
from logic.events.base import (
    ER,
    ET,
    EventHandler,
)


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(self, event: BaseEvent, event_handlers: Iterable[EventHandler[ET, ER]]):
        ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        ...
