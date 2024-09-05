from uuid import UUID
from dataclasses import dataclass
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound

class DeleteVideo:
    def __init__(self, repository: VideoRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        video = self.repository.get_by_id(id=input.id)
        if video is None:
            raise VideoNotFound(f"Video with {input.id} not found")

        self.repository.delete(video.id)
    