from uuid import UUID 
from dataclasses import dataclass
from pathlib import Path
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound, NotSupportedFile
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, ImageMedia, ImageSupportedFileFormat, VideoSupportedFileFormat
from src.core._shered.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shered.events.abstract_message_bus import AbstractMessageBus


class UploadVideo:

    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str # video/mp4 
        media_type: MediaType

    @dataclass
    class Output:
        pass 

    def __init__(
            self, 
            repository: VideoRepository,
            storage_service: AbstractStorageService,
            message_bus: AbstractMessageBus
        ):
        self.repository = repository
        self.storage_service = storage_service
        self.message_bus = message_bus
    
    def execute(self, input: Input) -> Output:
        video = self.repository.get_by_id(id=input.video_id)

        if video is None:
            raise VideoNotFound(f"Video with {input.video_id} not found") 
        
        if not input.media_type in MediaType:
            raise ValueError("media_type must be a valid Media Type: VIDEO, TRAILER, BANNER, THUMBNAIL and THUMBNAIL_HALF")

        file_extension = input.file_name.split('.')[-1].upper()
        if input.media_type in [MediaType.VIDEO.value, MediaType.TRAILER.value]:
            if not file_extension in VideoSupportedFileFormat:
                raise NotSupportedFile("Video extension file must be .mp4")
        else:
            if not file_extension in ImageSupportedFileFormat:
                raise NotSupportedFile("Image extension file must be .png")

        file_path = Path("videos") / str(video.id) / input.file_name
        self.storage_service.store(
            file_path=str(file_path), 
            content=input.content, 
            content_type=input.content_type
        )

        if input.media_type == MediaType.VIDEO.value or input.media_type == MediaType.TRAILER.value:
            audio_video_media = AudioVideoMedia(
                name=input.file_name,
                raw_location=str(file_path),
                encoded_location="",
                status=MediaStatus.PENDING,
                media_type=MediaType(input.media_type)
            )

            video.update_video_media(audio_video_media)
            self.repository.update(video, input.media_type)

            self.message_bus.handle([
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{video.id}.{audio_video_media.media_type.value}",
                    file_path = str(file_path)
                )
            ]) 
        else:
            image_media = ImageMedia(
                name=input.file_name,
                location=str(file_path),
            )
            
            if input.media_type == MediaType.BANNER.value:
                video.update_banner(image_media)
            elif input.media_type == MediaType.THUMBNAIL.value:
                video.update_thumbnail(image_media) 
            elif input.media_type == MediaType.THUMBNAIL_HALF.value: 
                video.update_thumbnail_half(image_media)
            
            self.repository.update(video, input.media_type)