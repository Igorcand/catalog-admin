from src.core._shered.events.abstract_message_bus import AbstractMessageBus
from src.core._shered.events.event import Event

class MessageBus(AbstractMessageBus):
    def handle(self, events: list[Event]) -> None:
        print(f"Handling events: {events}")