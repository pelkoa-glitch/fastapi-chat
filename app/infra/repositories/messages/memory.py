from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    List,
)

from domain.entities.messages import Chat
from infra.repositories.filters.messages import GetAllChatsFilters
from infra.repositories.messages.base import BaseChatsRepository


@dataclass
class MemoryChatRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(
        default_factory=list,
        kw_only=True,
    )

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(
                chat for chat in self._saved_chats if chat.oid == oid
            )

        except StopIteration:
            return None

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat for chat in self._saved_chats if chat.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def get_all_chats(self, filters: GetAllChatsFilters) -> tuple[List[Chat], Any]:
        return self._saved_chats, len(self._saved_chats)

    async def delete_chat_by_oid(self, chat_oid: str) -> None:
        chat = await self.get_chat_by_oid(chat_oid)

        if chat:
            self._saved_chats.remove(chat)
