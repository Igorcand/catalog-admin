
from dataclasses import dataclass, field
from decimal import Decimal
from src.core._shered.domain.entity import Entity
from uuid import UUID
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
    aggregate_id: UUID
    file_path: str
    media_type: MediaType