from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    title: str
    test: str
    # TODO: user_id если появится авторизация
