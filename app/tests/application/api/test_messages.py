from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response


@pytest.mark.asyncio
async def test_create_chat_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text()[:100]
    response: Response = client.post(url=url, json={'title': title})

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED, response.json()

    json_data = response.json()
    assert json_data['title'] == title


@pytest.mark.asyncio
async def test_create_chat_fail_text_too_long(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text(max_nb_chars=500)
    response: Response = client.post(url=url, json={'title': title})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_create_chat_fail_text_empty_title(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for('create_chat_handler')
    response: Response = client.post(url=url, json={'title': ''})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_create_message_chat_does_not_exist(
    app: FastAPI,
    client: TestClient,
    faker: Faker,

):
    chat_oid = 'uuid that does not exist in db'
    url = app.url_path_for('create_message_handler', chat_oid=chat_oid)

    text = faker.text()
    response: Response = client.post(url=url, json={'text': text, 'is_manager': False})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_delete_chat_by_oid_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text()
    response: Response = client.post(url=url, json={'title': title})

    json_data = response.json()

    chat_oid = json_data['oid']

    url = app.url_path_for('delete_chat_handler', chat_oid=chat_oid)
    delete_response: Response = client.delete(url=url)

    assert delete_response.is_success
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT, delete_response.json()


@pytest.mark.asyncio
async def test_check_delete_chat_thad_not_exists(
    app: FastAPI,
    client: TestClient,
):
    chat_oid = 'oid of the chat thet not exists'
    url = app.url_path_for('delete_chat_handler', chat_oid=chat_oid)
    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    json_data = response.json()

    assert json_data['detail']['error']
