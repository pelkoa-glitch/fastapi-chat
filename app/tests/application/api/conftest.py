from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from application.api.main import create_app
from logic.init import init_container
from tests.init_for_tests import init_container as test_container


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = test_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
