from decimal import Decimal
from uuid import UUID 
from dataclasses import dataclass
from src.core.video.domain.video import Video
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.video_repository import VideoRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

from src.core._shered.domain.notification import Notification

class CreateVideoWithoutMedia:

    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: str
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]
    
    @dataclass
    class Output:
        id: UUID
    
    def __init__(self, repository: VideoRepository, category_repository: CategoryRepository, genre_repository: GenreRepository, cast_member_repository: CastMemberRepository) -> None:
        self.repository = repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository


    def validate_categories(self, input: Input, notification:Notification) -> None:
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            notification.add_error(
                f"Categories not found: {input.categories - category_ids}"
            )
    
    def validate_genres(self, input: Input, notification:Notification) -> None:
        genres_ids = {genre.id for genre in self.genre_repository.list()}
        if not input.categories.issubset(genres_ids):
            notification.add_error(
                f"Genres not found: {input.genres - genres_ids}"
            )
    
    def validate_cast_members(self, input: Input, notification:Notification) -> None:
        cast_member_ids = {cast_member.id for cast_member in self.cast_member_repository.list()}
        if not input.cast_members.issubset(cast_member_ids):
            notification.add_error(
                f"Cast Member not found: {input.cast_member - cast_member_ids}"
            )

    def execute(self, input: Input) -> Output:
        notification = Notification()

        self.validate_categories(input, notification)
        self.validate_genres(input, notification)
        self.validate_cast_members(input, notification)
        
        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                duration=False,
                rating=input.rating,
                categories=input.categories,
                tigenrestle=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as err:
            raise InvalidVideo(err)

        self.repository.save()
        return self.Output(id=video.id)