from application.api.messages.filters import GetMessagesFilterss
from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageScherma,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetChatDetailQuery,
    GetMessagesQuery,
)
from punq import Container


router = APIRouter(tags=['Chat'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Endpoint creates a new chat, if a chat with this name exists, then 400 error is returned',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },

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
    '/{chat_oid}',
    status_code=status.HTTP_201_CREATED,
    description='Endpoint return chat',
    responses={
        status.HTTP_201_CREATED: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
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
    status_code=status.HTTP_201_CREATED,
    description='Endpoint return all messages in chat',
    responses={
        status.HTTP_201_CREATED: {'model': GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilterss = Depends(),
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
