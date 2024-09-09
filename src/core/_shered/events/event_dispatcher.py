from abc import ABC, abstractmethod
from src.core._shered.events.event import Event

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: Event) -> None:
        pass 


