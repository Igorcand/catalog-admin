from dataclasses import dataclass
from src.core._shered.events.event import Event

@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str # "<id>.<MediaType>" -> "34895-61308hbf-rjh02difh-p34y58.VIDEO"
    file_path: str 