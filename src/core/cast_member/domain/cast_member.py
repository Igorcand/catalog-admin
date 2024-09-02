from dataclasses import dataclass, field
from enum import StrEnum
import uuid
from uuid import UUID
from src.core._shered.entity import Entity

class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name cannot be longer than 255")

        if not self.name:
            self.notification.add_error("name cannot be empty")

        if not self.type in CastMemberType:
            self.notification.add_error("type must be a valid CastMemberType: actor or director")
        
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.type}"

    def __repr__(self):
        return f"<CastMember {self.name} {self.type} ({self.id})>"

    def update_cast_member(self, name, type):
        self.name = name
        self.type = type

        self.validate()