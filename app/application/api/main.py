from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aiojobs import Scheduler
from elasticapm.contrib.starlette import (
    ElasticAPM,
    make_apm_client,
)
from punq import Container

from application.api.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)
from application.api.messages.handlers import router as message_router
from application.api.messages.websockets.messages import router as message_ws_router
from logic.init import init_container
from settings.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)

    job = await scheduler.spawn(consume_in_background())

    yield
    await close_message_broker()
    await job.close()


def create_app() -> FastAPI:
    container: Container = init_container()
    config: Config = container.resolve(Config)

    app = FastAPI(
        title='Suppot Chat',
        description='',
        docs_url='/api/docs',
        debug=False,
        lifespan=lifespan,
    )
    app.include_router(message_router, prefix='/chats')
    app.include_router(message_ws_router, prefix='/chats')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ElasticAPM, client=make_apm_client(config.APM_SETTINGS))

    return app
