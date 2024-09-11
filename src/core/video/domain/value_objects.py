from dataclasses import dataclass
from uuid import UUID
from enum import Enum, auto, unique

@unique
class MediaStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

@unique
class Rating(Enum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"

@unique
class MediaType(Enum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"
    BANNER = "BANNER"

@unique
class VideoSupportedFileFormat(Enum):
    MP4 = "MP4"

@unique
class ImageSupportedFileFormat(Enum):
    PNG = "PNG"

@dataclass(frozen=True)
class ImageMedia:
    name: str
    location: str

@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType