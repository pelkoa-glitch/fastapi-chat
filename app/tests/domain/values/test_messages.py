from datetime import datetime
import pytest

from domain.exceptions.messages import EmptyTextException, TitleTooLongException
from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message


def test_create_message_success():
    text = Text('Hi zyabls')
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()

def test_create_message_empty_text_error():
    with pytest.raises(EmptyTextException):
        text = Text('')

def test_create_chat_success():
    title = Title('title')
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()

def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        title = Title('a' * 256)

def test_add_message_to_chat_success():
    text = Text('Hi zyabls')
    message = Message(text=text)

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages