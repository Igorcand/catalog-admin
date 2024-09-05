from uuid import UUID
from dataclasses import dataclass
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound
from decimal import Decimal
from src.core.video.domain.value_objects import Rating




class GetVideo:
    def __init__(self, repository: VideoRepository) -> None:
        self.repository = repository
    
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
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


    def execute(self, input: Input) -> Output:

        video = self.repository.get_by_id(id=input.id)

        if video is None:
            raise VideoNotFound(f"Video with {input.id} not found")

        return self.Output(
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

            )
    