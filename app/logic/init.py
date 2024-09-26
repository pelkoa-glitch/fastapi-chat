from functools import lru_cache

from infra.repositories.messages import (
    BaseChatRepository,
    MemoryChatRepository,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreteChatCommandHandler,
)
from logic.mediator import Mediator
from punq import (
    Container,
    Scope,
)


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container():
    container = Container()

    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreteChatCommandHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreteChatCommandHandler)],

        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
