from fastapi import FastAPI


def create_app():
    return FastAPI(
        title='Simple Fastapi Kafka Chat',
        description='FastAPI + KAFKA + DDD,',
        docs_url='/api/docs',
        debug=True
)
