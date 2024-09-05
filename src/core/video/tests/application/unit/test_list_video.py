from decimal import Decimal
from uuid import uuid4
from src.core.video.domain.value_objects import Rating
from src.core.video.application.use_cases.list_videos import ListOutput, ListVideo, VideoOutput
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from unittest.mock import create_autospec
from src.core._shered.domain.pagination import ListOutputMeta
import pytest

@pytest.mark.video
class TestListVidewo:
    def test_list_video_should_success(self):
        
        genre_repository = create_autospec(VideoRepository)

        video_1 = Video(
            title="Sample Video1",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_2 = Video(
            title="Sample Video2",
            description="A test video description",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        genre_repository.list.return_value = [video_1, video_2]


        use_case = ListVideo(repository=genre_repository)
        output = use_case.execute(ListVideo.Input())

        assert output == ListVideo.Output(
            data=[
                VideoOutput(
                    id=video_1.id,
                    title="Sample Video1",
                    description="A test video",
                    launch_year=2022,
                    duration=Decimal("120.5"),
                    opened=False,
                    published=False,
                    rating=Rating.AGE_14,
                    categories=set(),
                    genres=set(),
                    cast_members=set()
                ),
                VideoOutput(
                    id=video_2.id,
                    title="Sample Video2",
                    description="A test video description",
                    launch_year=2022,
                    duration=Decimal("120.5"),
                    opened=False,
                    published=False,
                    rating=Rating.AGE_12,
                    categories=set(),
                    genres=set(),
                    cast_members=set()
                ),
            ],
            meta = ListOutputMeta(current_page=1, per_page=2, total=2)
        )

