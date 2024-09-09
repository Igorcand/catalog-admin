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
            handlers = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(str(e))
    
    def register(self, event_type: Type[Event], handler: Handler) -> None:
        self.handlers[event_type].append(handler)