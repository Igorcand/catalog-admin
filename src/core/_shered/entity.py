from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from src.core._shered.notification import Notification

@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        return self.id == value.id

    @abstractmethod
    def validate(self):
        pass