from application.api.messages.handlers import router as message_router
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Fastapi Kafka Chat',
        description='FastAPI + KAFKA + DDD,',
        docs_url='/api/docs',
        debug=True,
    )
    app.include_router(message_router, prefix='/chat')

    return app
