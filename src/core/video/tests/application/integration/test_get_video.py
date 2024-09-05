import pytest 
from decimal import Decimal
from uuid import uuid4
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository

from src.core.video.domain.video import Video
from src.core.video.application.use_cases.get_video import GetVideo
from src.core.video.application.use_cases.exceptions import VideoNotFound


@pytest.mark.video
class TestGetVideo:
    def test_get_video_not_existing_should_error(self):
        
        repository = InMemoryVideoRepository()
        use_case = GetVideo(repository=repository)
        
        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(GetVideo.Input(id=uuid4()))
        
    def test_get_exisiting_video_should_success(self):
        
        repository = InMemoryVideoRepository()
        video = Video(
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
        repository.save(video)
        use_case = GetVideo(repository=repository)
        output = use_case.execute(GetVideo.Input(id=video.id))

        assert output == GetVideo.Output(
            id=video.id,
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            published=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set()

        )
        
        
    
    