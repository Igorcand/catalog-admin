from dataclasses import dataclass
from uuid import UUID
from enum import Enum, auto, unique

@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_19 = auto()

@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str 
    name: str
    location: str

@dataclass(frozen=True)
class AudioVideoMedia:
    id: UUID
    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus