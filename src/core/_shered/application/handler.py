from abc import ABC, abstractmethod
from src.core._shered.events.event import Event

class Handler(ABC):
    @abstractmethod
    def handle(self, events: Event) -> None:
        pass
