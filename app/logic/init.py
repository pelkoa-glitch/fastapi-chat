from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import (
    CreateChatCommand,
    CreteChatCommandHandler,
)
from logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    mediator.register_command(
        CreateChatCommand,
        [CreteChatCommandHandler(chat_repository=chat_repository)],
    )
