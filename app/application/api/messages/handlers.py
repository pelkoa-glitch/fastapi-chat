from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from punq import Container

from application.api.messages.filters import (
    GetAllChatsFilters,
    GetMessagesFilters,
)
from application.api.messages.schemas import (
    AddTelegramListenerResponseSchema,
    AddTelegramListenerSchema,
    ChatDetailSchema,
    ChatListenerItemSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageScherma,
    GetAllChatsQueryResponceSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import (
    AddTelegramListenerCommand,
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetAllChatListenersQuery,
    GetAllChatsQuery,
    GetChatDetailQuery,
    GetMessagesQuery,
)


router = APIRouter(tags=['Chat'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Endpoint creates a new chat, if a chat with this name exists, then 400 error is returned',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Create chat',
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Creates a new chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    description='Endpoint adds a new message to a chat',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Add message to a chat',
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageScherma,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Add a new message to a chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    description='Endpoint return chat',
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get chat',
)
async def get_chat_with_messages_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> ChatDetailSchema:
    """Return chat and all its messages."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return ChatDetailSchema.from_entity(chat)


@router.get(
    '/{chat_oid}/messages',
    status_code=status.HTTP_200_OK,
    description='Endpoint return all messages from chat',
    responses={
        status.HTTP_200_OK: {'model': GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get all messages from chat',
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),

) -> GetMessagesQueryResponseSchema:
    """Return all messages in chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Endpoint return all chats',
    responses={
        status.HTTP_200_OK: {'model': GetAllChatsQueryResponceSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get all chats',
)
async def get_all_chats_handler(
    filters: GetAllChatsFilters = Depends(),
    container: Container = Depends(init_container),

) -> GetAllChatsQueryResponceSchema:
    """Return all chats."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chats, count = await mediator.handle_query(
            GetAllChatsQuery(filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return GetAllChatsQueryResponceSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ChatDetailSchema.from_entity(chat) for chat in chats],
    )


@router.delete(
    '/{chat_oid}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete chat after conversation ends',
    description='Deletes chat by provided "chat_oid"',
)
async def delete_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteChatCommand(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.post(
    '/{chat_oid}/listeners/',
    status_code=status.HTTP_201_CREATED,
    summary='Add telegram support listeners to chat',
    description='Add telegram support listeners to chat',
    operation_id='addTelegramListenerToChat',
    response_model=AddTelegramListenerResponseSchema,
)
async def add_chat_listener_handler(
    chat_oid: str,
    schema: AddTelegramListenerSchema,
    container: Container = Depends(init_container),
) -> AddTelegramListenerResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        listener, *_ = await mediator.handle_command(
            AddTelegramListenerCommand(
                chat_oid=chat_oid,
                telegram_chat_id=schema.telegram_chat_id,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return AddTelegramListenerResponseSchema.from_entity(listener)


@router.get(
    '/{chat_oid}/listeners/',
    status_code=status.HTTP_200_OK,
    description='Get all chat listeners',
    responses={
        status.HTTP_200_OK: {'model': list[ChatListenerItemSchema]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get all chat listeners',
    operation_id='getAllChatListeners',
)
async def get_all_chats_listeners_handler(
    chat_oid: str,
    container: Container = Depends(init_container),

) -> list[ChatListenerItemSchema]:
    """Return all chats."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat_listeners = await mediator.handle_query(
            GetAllChatListenersQuery(chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return [ChatListenerItemSchema.from_entity(chat_listener=chat_listener) for chat_listener in chat_listeners]
