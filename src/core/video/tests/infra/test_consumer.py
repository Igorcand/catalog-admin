from src.core.video.infra.video_converted_rabbitmq_consumer import VideoConvertedRabbitMQConsumer
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
import pytest
from src.core.video.domain.video_repository import VideoRepository
from unittest.mock import create_autospec
import json
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaStatus, MediaType
from src.core.video.domain.video import Video, AudioVideoMediaUpdated
from decimal import Decimal 
from uuid import uuid4

@pytest.fixture
def video() -> Video:
    return Video(
        title="Sample Video",
        description="A test video",
        launch_year=2022,
        duration=Decimal("120.5"),
        opened=False,
        rating=Rating.AGE_12,
        categories={uuid4()},
        genres={uuid4()},
        cast_members={uuid4()},
    )

@pytest.mark.infra
class TestVideoConvertedConsumer:
    def test_on_message_method_video_converted_with_error_message(self):
        mock_video_repository = create_autospec(VideoRepository)
        consumer = VideoConvertedRabbitMQConsumer(video_repository=mock_video_repository)
        message = {
            "error": "error_message",
            "video": {
                "resource_id": "24846fe1-6218-46bb-96a8-d6d4534e0885.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video"
            },
            "status": "ERROR"
        }
        consumer.on_message(json.dumps(message))

        mock_video_repository.update.assert_not_called()
    
    def test_on_message_method_video_converted_with_valid_message(self, video: Video):

        video.video = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO
        )

        mock_video_repository = create_autospec(VideoRepository)
        mock_video_repository.get_by_id.return_value = video
        mock_video_repository.update.return_value = None

        consumer = VideoConvertedRabbitMQConsumer(video_repository=mock_video_repository)
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video.id}.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video"
            },
            "status": "COMPLETED"
        }
        consumer.on_message(json.dumps(message))

        mock_video_repository.get_by_id.assert_called_once_with(video.id)
        mock_video_repository.update.assert_called_once_with(video, MediaType.VIDEO)


