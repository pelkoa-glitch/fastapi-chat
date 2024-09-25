from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f'Сould not find handlers for the event {self.event_type}.'


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f'Сould not find handlers for the command {self.command_type}.'
