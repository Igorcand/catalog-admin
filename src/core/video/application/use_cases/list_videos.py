from uuid import UUID
from dataclasses import dataclass
from src.core.video.domain.video_repository import VideoRepository
from enum import StrEnum
from src.core._shered.domain.pagination import ListOutputMeta, ListOutput
from src import config
from decimal import Decimal
from src.core.video.domain.value_objects import Rating

class VideoFilterByType(StrEnum):
    NAME = "name"

@dataclass
class VideoOutput:
    id: UUID
    title: str
    description: str 
    launch_year: int 
    duration: Decimal
    rating: Rating 
    opened: bool
    published: bool
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

class ListVideo:
    def __init__(self, repository: VideoRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        order_by: VideoFilterByType = ""
        current_page: str = 1

    @dataclass
    class Output(ListOutput[VideoOutput]):
        pass


    def execute(self, input: Input):
        videos = self.repository.list()

        mapped_videos = [
            VideoOutput(
                id = video.id,
                title = video.title,
                description = video.description,
                launch_year = video.launch_year, 
                duration = video.duration,
                rating = video.rating,
                opened = video.opened,
                published = video.published,
                categories=video.categories,
                genres=video.genres,
                cast_members=video.cast_members,
            ) for video in videos
        ]
        if input.order_by:
            if input.order_by and input.order_by in VideoFilterByType:
                mapped_videos = sorted(mapped_videos, key=lambda video: getattr(video, input.order_by))
        
        page_offset = (input.current_page -1) * config.DEFAULT_PAGE_SIZE
        videos_page = mapped_videos[page_offset:page_offset+config.DEFAULT_PAGE_SIZE]

        return self.Output(
            data=videos_page,
            meta = ListOutputMeta(
                current_page = input.current_page,
                per_page = config.DEFAULT_PAGE_SIZE,
                total = len(mapped_videos)
            )
            )