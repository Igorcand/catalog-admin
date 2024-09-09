from typing import Type
from src.core._shered.application.handler import Handler
from src.core._shered.events.abstract_message_bus import AbstractMessageBus
from src.core._shered.events.event import Event

class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {}

    def handle(self, events: list[Event]) -> None:
        print(f"Handling events: {events}")
        for event in events:
            for handler in self.handlers[type(event)]:
                handler.handle(event)