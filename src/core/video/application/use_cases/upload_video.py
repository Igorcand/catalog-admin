from uuid import UUID 
from dataclasses import dataclass
from pathlib import Path
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core._shered.infrastructure.storage.abstract_storage_service import AbstractStorageService


class UploadVideo:

    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str # video/mp4 

    @dataclass
    class Output:
        pass 

    def __init__(
            self, 
            repository: VideoRepository,
            storage_service: AbstractStorageService
        ):
        self.repository = repository
        self.storage_service = storage_service
    
    def execute(self, input: Input) -> Output:
        video = self.repository.get_by_id(id=input.video_id)

        if video is None:
            raise VideoNotFound(f"Video with {input.video_id} not found") 

        file_path = Path("videos") / str(video.id) / input.file_name
        self.storage_service.store(
            file_path=str(file_path), 
            content=input.content, 
            content_type=input.content_type
        )

        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING
        )

        video.update_video_media(audio_video_media)

        self.repository.update(video)