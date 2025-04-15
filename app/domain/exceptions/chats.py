from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class ListenerAlredyExistsException(ApplicationException):
    listener_oid: str

    @property
    def message(self):
        return 'Listener alredy listens that'
