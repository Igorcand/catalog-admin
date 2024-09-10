from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating, AudioVideoMedia, MediaStatus, MediaType
from decimal import Decimal
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core._shered.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core._shered.events.abstract_message_bus import AbstractMessageBus
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from unittest.mock import create_autospec
from uuid import uuid4
import pytest
from src.core.video.application.use_cases.exceptions import VideoNotFound

@pytest.mark.video
class TestUploadVideo:
    def test_when_video_does_not_exist_then_raise_error(self):
        video_repository = InMemoryVideoRepository()
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        ) 
        
        input = UploadVideo.Input(
                video_id=uuid4(),
                file_name="video.mp4",
                content=b"video_content",
                content_type="video/mp4",
            )
        
        with pytest.raises(VideoNotFound) as exc:
            use_case.execute(input=input)

    def test_upload_video_media_to_video(self):
        video =  Video(
                title="Sample Video",
                description="A test video",
                launch_year=2022,
                duration=Decimal("120.5"),
                opened=False,
                rating=Rating.AGE_12,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )
        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        ) 
        
        input = UploadVideo.Input(
                video_id=video.id,
                file_name="video.mp4",
                content=b"video_content",
                content_type="video/mp4",
            )
        

        use_case.execute(input=input)

        mock_storage.store.assert_called_once_with(
            file_path=f"videos/{video.id}/video.mp4",
            content=b"video_content",
            content_type="video/mp4",
        )

        mock_message_bus.handle.assert_called_once_with(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{video.id}.{MediaType.VIDEO.value}",
                    file_path=f"videos/{video.id}/video.mp4"
                )
            ]
        )

        video_from_repo = video_repository.get_by_id(video.id)
        video_from_repo.video = AudioVideoMedia(
            name="video.mp4",
            raw_location=f"videos/{video.id}/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )
    
    