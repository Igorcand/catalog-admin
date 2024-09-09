from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from src.core._shered.domain.notification import Notification
from src.core._shered.events.event import Event
from src.core._shered.events.abstract_message_bus import AbstractMessageBus
from src.core._shered.events.message_bus import MessageBus


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification)

    events: list[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory = MessageBus)

    def dispatch(self, event: Event) -> None:
        self.events.append(event)
        self.message_bus.handle(self.events)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        return self.id == value.id

    @abstractmethod
    def validate(self):
        pass